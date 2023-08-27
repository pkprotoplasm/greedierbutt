import sys
import requests
import json
from datetime import datetime, timedelta
import time
import logging
from celery import shared_task

# Flask imports
from flask import current_app as app
from flask import g

# Application imports
from greedierbutt_flask import dbConn

logger = logging.getLogger(__name__)

@shared_task(name='jobs.profiles.scheduled_profile_pull')
def scheduled_profile_pull(span='default'):
    results = []

    try:
        results.append(pull_player_profiles(span))
    except Exception as e:
        logger.error(f"scheduled_profile_pull({span}): Exception: {e}")

    return results

@shared_task(bind=True, name='jobs.profiles.update_banned_user_profile')
def update_banned_user_profile(self, reportid, steamid, reason):
    cursor = dbConn.connection.cursor()    
    cursor.execute('UPDATE profiles AS p, reports AS r SET p.blacklisted=1, p.blacklisted_date=NOW(), p.blacklisted_by=%s, p.blacklisted_reason=%s WHERE p.steamid=r.steamid AND r.reportid=%s', [steamid, reason, reportid])

    dbConn.connection.commit()
    cursor.close()
    return f"Successfully updated banned user profile for report {reportid}"

@shared_task(bind=True, name='jobs.profiles.insert_dummy_profiles', autoretry_for=(Exception,), retry_backoff=10, retry_kwargs={'max_retries': 5})
def insert_dummy_profiles(self, profile_list):
    cursor = dbConn.connection.cursor()    
    cursor.executemany("INSERT IGNORE INTO profiles (steamid, personaname) VALUES (%s, 'Unknown user')", profile_list)

    dbConn.connection.commit()
    cursor.close()
    return f"Successfully inserted dummy profile for Steam ID(s) {profile_list}"

@shared_task(bind=True, name='jobs.profiles.automod_ban_profile', autoretry_for=(Exception,), retry_backoff=10, retry_kwargs={'max_retries': 5})
def automod_ban_profile(self, steamid, reason):
    cursor = dbConn.connection.cursor()
    cursor.execute("INSERT INTO profiles (steamid, blacklisted, blacklisted_by, blacklisted_reason, blacklisted_date) VALUES(%s, true, 0, %s, TIMESTAMP(NOW())) ON DUPLICATE KEY UPDATE blacklisted=true, blacklisted_by=0, blacklisted_reason=%s", (steamid, reason, reason))

    dbConn.connection.commit()
    cursor.close()
    return f"Successfully set automod ban for Steam ID {steamid}"

@shared_task(bind=True, name='jobs.profiles.update_steam_profile', autoretry_for=(Exception,), retry_backoff=10, retry_kwargs={'max_retries': 5})
def update_steam_profile(self, steamid, personaname, profileurl, avatar, avatarmedium, avatarfull):
    cursor = dbConn.connection.cursor()
    
    # Update the player's profile stored in our database.
    cursor.execute("UPDATE profiles SET personaname=%s, profileurl=%s, avatar=%s, avatarmedium=%s, avatarfull=%s WHERE steamid=%s", [personaname, profileurl, avatar, avatarmedium, avatarfull, steamid])
    dbConn.connection.commit()
    cursor.close()

    return f"Successfully updated profile from Steam for {steamid}"

def pull_player_profiles(span='all'):
    with app.app_context():
        try:
            cursor = dbConn.connection.cursor()

            todays_date = datetime.now() - timedelta(hours=5)
            yesterdays_date = datetime.now() - timedelta(days=1, hours=5)

            if span == 'all':
                # Called with "all" on the daily switchover. Just grabs 50k random most-oudated profiles to update. This results in up to 500 API calls.
                cursor.execute("""SELECT steamid FROM profiles WHERE lastupdate < timestamp(now() - interval 24 hour) order by lastupdate ASC, rand() ASC LIMIT 50000""")
            else:
                # No args on the 10-minute interval invocation. Grabs today and yesterday's unique players. Tends to be between 10-20k (100-200 API calls per run or up to 30k API calls per day).
                # Limit to 30,000 per invocation to be safe (up to 43,200 API calls in a day).
                cursor.execute("""with activeplayers as (select distinct steamid from scores where date=%s or date=%s) select distinct p.steamid from profiles p, activeplayers a where p.steamid=a.steamid and (p.lastupdate < timestamp(now() - interval 1 hour) or p.personaname='Unknown User') order by rand() limit 30000""", (todays_date.strftime("%Y%m%d"), yesterdays_date.strftime("%Y%m%d")))

            profileRows = cursor.fetchall()

            apiCallCount = 0
            retryCount = 0
            insertList = []

            for i in range(0, len(profileRows), 100):
                apiCallURL = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={app.config.get('STEAM_KEY')}&steamids="
                for profileRow in profileRows[i:i+100]:
                    apiCallURL = f'{apiCallURL}{profileRow["steamid"]},'
                apiCallURL = apiCallURL[:-1]

                while True:
                    try:
                        time.sleep(2) # Sleep two seconds to avoid ratelimits.
                        profilesPayload = requests.get(apiCallURL)
                        profiles = json.loads(profilesPayload.text)
                        apiCallCount += 1
                        break
                    except Exception as e:
                        if profilesPayload.status_code == 429:
                            logger.info(f"pull_player_profiles({span}): Steam API said too many requests")
                            if i == 0 or retryCount > 10:
                                logger.info(f"pull_player_profiles({span}): API Limit is exceeded.")
                                break
                            retryCount += 1
                            time.sleep(60)
                        pass

                for playerProfile in profiles["response"]["players"]:
                    insertList.append((playerProfile["personaname"], playerProfile["profileurl"], playerProfile["avatar"], playerProfile["avatarmedium"], playerProfile["avatarfull"], playerProfile["steamid"], playerProfile["personaname"], playerProfile["profileurl"], playerProfile["avatar"], playerProfile["avatarmedium"], playerProfile["avatarfull"]))

            if len(insertList) > 0:
                cursor.executemany("""INSERT INTO profiles(personaname, profileurl, avatar, avatarmedium, avatarfull, steamid, blacklisted) VALUES(%s, %s, %s, %s, %s, %s, false) ON DUPLICATE KEY UPDATE personaname=%s, profileurl=%s, avatar=%s, avatarmedium=%s, avatarfull=%s, lastupdate=TIMESTAMP(NOW())""", insertList)

            cursor.execute("""UPDATE metadata SET lastupdate=TIMESTAMP(NOW())""")

            dbConn.connection.commit()
            cursor.close()

            return f"Successfully updated {len(insertList)} profiles (considered {len(profileRows)} active players)"
        except Exception as e:
            logger.error(f"ERROR: pull_player_profiles({span}) #{sys.exc_info()[-1].tb_lineno}: Exception: {e}")