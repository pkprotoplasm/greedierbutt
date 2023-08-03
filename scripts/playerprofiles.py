#!/usr/bin/python3

from concurrent.futures import process
import sys
import MySQLdb
import MySQLdb.cursors
import requests
import json
import time
from datetime import datetime, timedelta
import fasteners, threading
from os import path

sys.path.append(path.dirname(path.realpath(__file__)))

from config import Config

mysqlpass=Config.MYSQL_WRITE_PASSWORD
mysqldb=Config.MYSQL_DB

lock = fasteners.InterProcessLock('/tmp/gbpp.lock')

lockres = lock.acquire(timeout=1)

if lockres == False:
    #print(f'Another instance of {sys.argv[0]} is currently running. Exiting.', file=sys.stderr)
    sys.exit(1)

steamAPIKey = Config.STEAM_KEY

greedierdb = MySQLdb.connect(passwd=mysqlpass, database=mysqldb, cursorclass = MySQLdb.cursors.SSCursor, connect_timeout=10)
scorecursor = greedierdb.cursor()
profilecursor = greedierdb.cursor()

profilecursor.execute("SET interactive_timeout=3600")
profilecursor.execute("SET wait_timeout=3600")

todaysDate = datetime.now() - timedelta(hours=5)
yesterdaysDate = datetime.now() - timedelta(days=1, hours=5)


updateProfiles = []

if len(sys.argv) > 1 and sys.argv[1] == "all":
    # Called with "all" on the daily switchover. Just grabs 200k random un-updated profiles to update. This results in up to 2,000 API calls.
    profilecursor.execute("""SELECT steamid FROM profiles WHERE lastupdate < now() - interval 24 hour order by rand() LIMIT 200000""")
else:
    # No args on the 10-minute interval invocation. Grabs today and yesterday's unique players. Tends to be between 10-20k (100-200 API calls per run or up to 30k API calls per day).
    # Limit to 30,000 per invocation to be safe (up to 43,200 API calls in a day).
    profilecursor.execute("""with activeplayers as (select distinct steamid from scoresunion where date=%s or date=%s) select distinct p.steamid from profiles p, activeplayers a where p.steamid=a.steamid and (p.lastupdate < now() - interval 1 hour or p.personaname='Unknown User') order by rand() limit 30000""", (todaysDate.strftime("%Y%m%d"), yesterdaysDate.strftime("%Y%m%d")))

profileRows = profilecursor.fetchall()

# We disconnect at this point because the API calls will take a while. We'll reconnect later to avoid mysql timeout errors.
profilecursor.close()
greedierdb.close()

apiCallCount = 0
insertList = []

for i in range(0, len(profileRows), 100):
    apiCallURL = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamAPIKey + "&steamids="
    for steamid in profileRows[i:i+100][0]:
        apiCallURL = apiCallURL + str(steamid) + ","
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
                if i == 0:
                    print(f'{sys.argv[0]}: Received too many requests on first iteration. Exiting.', file=sys.stderr)
                    greedierdb.close()
                    sys.exit(-1)
                time.sleep(60)
            pass

    for playerProfile in profiles["response"]["players"]:
        insertList.append((playerProfile["personaname"], playerProfile["profileurl"], playerProfile["avatar"], playerProfile["avatarmedium"], playerProfile["avatarfull"], playerProfile["steamid"], playerProfile["personaname"], playerProfile["profileurl"], playerProfile["avatar"], playerProfile["avatarmedium"], playerProfile["avatarfull"]))

greedierdb = MySQLdb.connect(passwd=mysqlpass, database=mysqldb, cursorclass = MySQLdb.cursors.SSCursor, connect_timeout=10)
profilecursor = greedierdb.cursor()

for profile in insertList:
    profilecursor.execute("""INSERT INTO profiles(personaname, profileurl, avatar, avatarmedium, avatarfull, steamid, blacklisted) VALUES(%s, %s, %s, %s, %s, %s, false) ON DUPLICATE KEY UPDATE personaname=%s, profileurl=%s, avatar=%s, avatarmedium=%s, avatarfull=%s""", profile)

profilecursor.execute("""UPDATE metadata SET lastupdate=TIMESTAMP(NOW())""")

greedierdb.commit()
greedierdb.close()

lock.release()
