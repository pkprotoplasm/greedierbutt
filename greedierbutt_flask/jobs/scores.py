import sys
import requests
import xmltodict
from datetime import datetime, timedelta, date
import time
from os import path
import logging
from celery import shared_task


# Flask imports
from flask import current_app as app
from flask import g

# Application imports
from greedierbutt_flask import dbConn
from greedierbutt_flask.jobs.profiles import insert_dummy_profiles, automod_ban_profile

logger = logging.getLogger(__name__)

@shared_task(name='jobs.scores.scheduled_score_pull')
def scheduled_score_pull():
    """Scheduled task to pull scores for all three DLCs for the current date."""
    today = (datetime.utcnow() - timedelta(hours=10))

    results = []

    for dlc in ["rep", "abp", "ab"]:
        try:
            results.append(fetch_scores(date=today.strftime('%Y%m%d'), dlc=dlc))
        except Exception as e:
            logger.info(f"scheduled_score_pull(): Exception: {e}")

    return results

@shared_task(name='jobs.scores.scheduled_daily_lookback')
def scheduled_daily_lookback():
    """Scheduled task to pull scores for the past 7 days for all DLCs."""
    
    results = []

    for date_diff in range(0, 7, 1):

        cur_date = (datetime.utcnow() - timedelta(hours=13) - timedelta(days=date_diff))

        for dlc in ["rep", "abp", "ab"]:
            try:
                results.append(fetch_scores(date=cur_date.strftime('%Y%m%d'), dlc=dlc))
            except Exception as e:
                logger.info(f"scheduled_daily_lookback(): Exception: {e}")

    return results

@shared_task(name='jobs.scores.scheduled_daily_rerank')
def scheduled_daily_rerank():
    """Scheduled task to update ranks, excluding banned players."""
    results = []
    
    results.append(full_rerank())

    return results

@shared_task(name='jobs.scores.calculate_top100_noaltf4')
def scheduled_top100_noaltf4():
    """Scheduled task to calculate top-100 no alt+f4 leaderboards for the current date."""

    results = []
    for (dest_table, dlc) in [('toprankingsr', 'rep'), ('toprankingsabp', 'abp'), ('toprankingsab', 'ab')]:
        try:
            results.append(calculate_top100_noaltf4(dest_table, dlc))
        except Exception as e:
            logger.info(f"scheduled_top100_noaltf4(): Exception: {e}")

    return results

@shared_task(bind=True, name='jobs.scores.update_banned_user_scores', autoretry_for=(Exception,), retry_backoff=10, retry_kwargs={'max_retries': None})
def update_banned_user_scores(self, reportid):
    cursor = dbConn.connection.cursor()
    cursor.execute('UPDATE scores AS s, reports AS r SET s.scorerank=999999, s.timerank=999999 WHERE s.steamid=r.steamid AND r.reportid=%s', [reportid])
    
    dbConn.connection.commit()
    cursor.close()
    return f"Successfully updated scores for banned user on report {reportid}"
    
def get_date_url(dlc, date):
    """Returns steam leaderboard XML URL for a given date & dlc."""
    with open(f"{path.dirname(path.realpath(__file__))}/datescoreurls-{dlc}.txt", 'r') as dateURLs:
        dateURLPairs = dateURLs.readlines()

    for dateURLPairString in dateURLPairs:
        dateURLPair = dateURLPairString.split(':')
        if dateURLPair[1].strip() == date:
            return f"https://steamcommunity.com/stats/250900/leaderboards/{dateURLPair[0]}/?xml=1"

    return ''

def to_little(val):
    """Converts a hex number to little endian."""
    little_hex = bytearray.fromhex(val)
    little_hex.reverse()

    return ''.join(format(x, '02x') for x in little_hex)

def fetch_scores(date, dlc):
    """Background task to fetch scores from a given date for a given DLC."""

    with app.app_context():
        try:
            cursor = dbConn.connection.cursor()

            cursor.execute("SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode, 'ERROR_FOR_DIVISION_BY_ZERO', ''))")

            dateURL = get_date_url(dlc, date)

            processedRecords = 0
            while True:
                try:
                    leaderboardPayload = requests.get(dateURL)
                    leaderboard = xmltodict.parse(leaderboardPayload.content)
                    break
                except Exception as e:
                    logger.warn(f"WARN: fetch_scores({date}, {dlc}) #{sys.exc_info()[-1].tb_lineno}: {e}")
                    time.sleep(30)
                    pass

            insertList = []
            banList = []
            steamIDList = []

            if (leaderboard["response"]["resultCount"] == "0"):
                raise Exception("Steam returned an empty result set", "No records", 69) # Nice
            
            while True:
                for leaderboardEntry in leaderboard["response"]["entries"]["entry"]:
                    shortenedLine = 0
                    if leaderboardEntry["details"] is None:
                        scoreDetails = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                    else:
                        scoreDetails = str.ljust(str(leaderboardEntry["details"]), 112, '0') # To support older Afterbirth score lines which don't include some data.
                        if len(leaderboardEntry["details"]) < 112:
                            shortenedLine = 1

                    stageBonus = int(to_little(scoreDetails[0:8]), 16)
                    schwagBonus = int(to_little(scoreDetails[8:16]), 16)
                    bluebabyBonus = int(to_little(scoreDetails[16:24]), 16)
                    lambBonus = int(to_little(scoreDetails[24:32]), 16)
                    megasatanBonus = int(to_little(scoreDetails[32:40]), 16)
                    rushBonus = int(to_little(scoreDetails[40:48]), 16)
                    explorationBonus = int(to_little(scoreDetails[48:56]), 16)
                    damagePenalty = int(to_little(scoreDetails[56:64]), 16)
                    timePenalty = int(to_little(scoreDetails[64:72]), 16)
                    itemPenalty = int(to_little(scoreDetails[72:80]), 16)
                    level = int(to_little(scoreDetails[80:88]), 16)
                    timeTaken = int(to_little(scoreDetails[96:104]), 16)
                    goal = int(to_little(scoreDetails[104:112]), 16)

                    if timePenalty > 2147483647:
                        banList.append((int(leaderboardEntry["steamid"]), f"Impossible time penalty {timePenalty} on {date}"))

                    if schwagBonus > 19150:
                        banList.append((int(leaderboardEntry["steamid"]), f"Impossible schwag bonus {schwagBonus} on {date}"))

                    scoreKey = leaderboardEntry['steamid'] + '.' + date
                    
                    # The executemany() job will expect a tuple here.
                    steamIDList.append((int(leaderboardEntry['steamid']),))

                    insertList.append((int(date), scoreKey, int(leaderboardEntry["steamid"]), int(leaderboardEntry["rank"]), int(leaderboardEntry["score"]), stageBonus, explorationBonus, schwagBonus, rushBonus, bluebabyBonus, lambBonus, megasatanBonus, damagePenalty, timePenalty, itemPenalty, level, timeTaken, goal, leaderboardEntry["details"], shortenedLine, int(leaderboardEntry['rank']), int(leaderboardEntry["score"]), stageBonus, explorationBonus, schwagBonus, rushBonus, bluebabyBonus, lambBonus, megasatanBonus, damagePenalty, timePenalty, itemPenalty, level, timeTaken, goal, leaderboardEntry["details"], shortenedLine))

                processedRecords += int(leaderboard["response"]["resultCount"])

                if "nextRequestURL" in leaderboard["response"]:
                        while True:
                            try:
                                leaderboardPayload = requests.get(leaderboard["response"]["nextRequestURL"])
                                break
                            except Exception as e: 
                                time.sleep(30)
                                pass
                        leaderboard = xmltodict.parse(leaderboardPayload.content)
                else:
                    break

            # This loops in reverse because sometimes steam returns another score row for a player with all zeroes. This allows us to overwrite it with the higher actual score.
            insertListWithDLC = []
            for record in insertList[:-1]:
                recordWithDLC = list(record)
                recordWithDLC.pop(36)
                recordWithDLC.pop(19)
                recordWithDLC.pop(1)
                if dlc == "ab":
                    recordWithDLC.insert(18, "ab")
                    recordWithDLC.insert(37, "ab")
                elif dlc == "abp":
                    recordWithDLC.insert(18, "abp")
                    recordWithDLC.insert(37, "abp")
                else:
                    recordWithDLC.insert(18, "rep")
                    recordWithDLC.insert(37, "rep")
                insertListWithDLC.append(recordWithDLC)

            cursor.executemany("""
                INSERT INTO
                    scores
                    (
                        date,
                        steamid,
                        rank,
                        scorerank,
                        timerank,
                        score,
                        stage_bonus,
                        exploration_bonus,
                        schwag_bonus,
                        rush_bonus,
                        bluebaby_bonus,
                        lamb_bonus,
                        megasatan_bonus,
                        damage_penalty,
                        time_penalty,
                        item_penalty,
                        level,
                        time,
                        goal,
                        details,
                        dlc)
                    VALUES(%s, %s, %s, 0, 0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        rank=%s,
                        score=%s,
                        stage_bonus=%s,
                        exploration_bonus=%s,
                        schwag_bonus=%s,
                        rush_bonus=%s,
                        bluebaby_bonus=%s,
                        lamb_bonus=%s,
                        megasatan_bonus=%s,
                        damage_penalty=%s,
                        time_penalty=%s,
                        item_penalty=%s,
                        level=%s,
                        time=%s,
                        goal=%s,
                        details=%s,
                        dlc=%s
                """, insertListWithDLC)


            #### Rerank the current day's combined scores table.
            cursor.execute("""
                update
                    scores,
                (
                    SELECT
                        scores.scoreid,
                        scores.date,
                        scores.dlc,
                        rank() over(partition by scores.date, scores.dlc order by scores.score desc, scores.time asc) as scorerank,
                        rank() over(partition by scores.date, scores.dlc order by scores.level desc, scores.time asc, scores.score desc) as timerank
                    FROM
                        scores
                    INNER JOIN
                        profiles
                    ON
                        scores.steamid=profiles.steamid
                    WHERE
                        profiles.blacklisted=false and
                        scores.date=%(today)s
                ) as sr
                set
                    scores.scorerank=sr.scorerank,
                    scores.timerank=sr.timerank
                where
                    scores.scoreid=sr.scoreid and
                    scores.dlc=sr.dlc
            """, { 'today': date })

            cursor.execute("""
                UPDATE
                    scores AS s
                INNER JOIN
                    profiles AS p
                ON
                    s.steamid=p.steamid
                SET
                    s.scorerank=999999,
                    s.timerank=999999
                WHERE
                    p.blacklisted=true
            """)
            ####

            cursor.execute("""UPDATE metadata SET activeplayercount=(SELECT COUNT(DISTINCT steamid) FROM scores WHERE scorerank<999999 AND scorerank>0 AND goal>0)""")
            cursor.execute("""UPDATE metadata SET scorelinecount=(SELECT COUNT(scoreid) FROM scores)""")

            dbConn.connection.commit()

            cursor.close()

            insert_dummy_profiles.delay(profile_list=steamIDList)

            for profile in banList:
                automod_ban_profile.delay(steamid=profile[0], reason=profile[1])

            return f"Successfully fetched {date} for {dlc}"

        except Exception as e:
            logger.error(f"ERROR: fetch_scores({date}, {dlc}) #{sys.exc_info()[-1].tb_lineno}: {e}")
            return e


def calculate_top100_noaltf4(dest_table, dlc):
    """Background task to calculate the no alt+f4 leaderboard for a given dlc."""
    with app.app_context():
        try:
            cursor = dbConn.connection.cursor()

            start_date = f"{(date.today() - timedelta(days=91)):%Y%m%d}"
            end_date = f"{date.today():%Y%m%d}"

            # We won't use parameterization here because the input is necessarily safe and
            # parameterization can't be used for table names.
            cursor.execute(f"""delete from {dest_table}""")
            cursor.execute(f"""
                INSERT INTO
                    {dest_table}
                WITH
                    entries AS (
                        SELECT
                            steamid,
                            count(scoreid) as entrycount
                        FROM
                            scores
                        WHERE
                            date>={start_date} and
                            date<{end_date} and
                            score>0 and
                            time>0 and
                            dlc="{dlc}"
                        GROUP BY
                            steamid
                    ),
                    zeroes AS (
                        SELECT
                            steamid,
                            count(scoreid) as zerocount
                        FROM
                            scores
                        WHERE
                            date>={start_date} and
                            date<{end_date} and
                            score=0 and
                            time=0 and
                            dlc="{dlc}"
                        GROUP BY
                            steamid
                    ),
                    averages AS (
                        SELECT
                            scoresr.steamid as steamid,
                            avg(scoresr.scorerank) AS scorerank,
                            avg(scoresr.timerank) AS timerank,
                            avg(scoresr.scorepercentile) AS scorepercentile,
                            avg(scoresr.timepercentile) AS timepercentile
                        FROM
                            (
                            SELECT
                                s.scoreid, s.date, s.steamid, s.score, s.time,
                                RANK() OVER(partition by s.date order by s.score desc, s.time asc) AS scorerank,
                                RANK() OVER(partition by s.date order by s.level desc, s.time asc, s.score desc) AS timerank,
                                CUME_DIST() OVER(partition by s.date order by s.score desc, s.time asc) AS scorepercentile,
                                CUME_DIST() OVER(partition by s.date order by s.level desc, s.time asc, s.score desc) AS timepercentile
                            FROM
                                scores AS s
                            WHERE
                                s.date>={start_date} AND
                                s.date<{end_date} AND
                                s.score>0 AND
                                s.time>0 AND
                                s.dlc="{dlc}"
                            ) AS scoresr
                        GROUP BY
                            scoresr.steamid
                    )
                SELECT
                    entries.steamid AS steamid,
                    averages.scorerank AS avgscorerank,
                    averages.timerank AS avgtimerank,
                    (averages.scorepercentile*100) AS avgscorepercentile,
                    (averages.timepercentile*100) AS avgtimepercentile,
                    entries.entrycount AS entries,
                    zeroes.zerocount AS zerocount
                FROM
                    entries
                LEFT JOIN
                    profiles
                ON
                    profiles.steamid=entries.steamid
                LEFT JOIN
                    zeroes
                ON
                    zeroes.steamid=entries.steamid
                JOIN
                    averages
                ON
                    averages.steamid=entries.steamid
                WHERE
                    profiles.blacklisted=false and
                    entries.entrycount>=10 and
                    (
                        ((zeroes.zerocount/entries.entrycount)*100)<=10 or
                        zeroes.zerocount is null
                    )
            """)

            dbConn.connection.commit()
            cursor.close()

            return f"Successfully calculated no alt+f4 leaderboard for {dlc}"
        except Exception as e:
            logger.error(f"ERROR: calculate_top100_noaltf4({dlc}) #{sys.exc_info()[-1].tb_lineno}: {e}")
            return e

def full_rerank():
    """Background task to rerank all score lines, excluding banned players."""
    with app.app_context():
        try:
            cursor = dbConn.connection.cursor()
            cursor.execute("""UPDATE LOW_PRIORITY reports SET processed=true WHERE approved=true""")

            cursor.execute("""
                update
                    scores,
                (
                    SELECT
                        scores.scoreid,
                        scores.date,
                        scores.dlc,
                        rank() over(partition by scores.date, scores.dlc order by scores.score desc, scores.time asc) as scorerank,
                        rank() over(partition by scores.date, scores.dlc order by scores.level desc, scores.time asc, scores.score desc) as timerank
                    FROM
                        scores
                    INNER JOIN
                        profiles
                    ON
                        scores.steamid=profiles.steamid
                    WHERE
                        profiles.blacklisted=false and
                        scores.date in (
                            SELECT
                                distinct(sr2.date)
                            FROM
                                scores sr2
                            INNER JOIN
                                profiles p2
                            ON
                                p2.steamid=sr2.steamid
                            WHERE
                                p2.blacklisted_date>=%(today)s
                        ) and
                        scores.date<%(today)s
                ) as sr
                set
                    scores.scorerank=sr.scorerank,
                    scores.timerank=sr.timerank
                where
                    scores.scoreid=sr.scoreid and
                    scores.dlc=sr.dlc
            """, { 'today': f"{date.today():%Y%m%d}" })

            cursor.execute("""
                UPDATE
                    scores AS s
                INNER JOIN
                    profiles AS p
                ON
                    s.steamid=p.steamid
                SET
                    s.scorerank=999999,
                    s.timerank=999999
                WHERE
                    p.blacklisted=true
            """)

            cursor.execute("""UPDATE LOW_PRIORITY metadata SET lastupdate=TIMESTAMP(NOW())""")

            dbConn.connection.commit()
            cursor.close()

            return "Successfully updated ranks"
        except Exception as e:
            logger.error(f"ERROR: full_rerank() #{sys.exc_info()[-1].tb_lineno}: {e}")
            return e