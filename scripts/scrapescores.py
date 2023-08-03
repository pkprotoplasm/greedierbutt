#!/usr/bin/python3

import sys
import MySQLdb
import MySQLdb.cursors
import requests
import xmltodict
import time
from os import path

sys.path.append(path.dirname(path.realpath(__file__)))

from config import Config

mysqlpass=Config.MYSQL_PASSWORD
mysqldb=Config.MYSQL_DB

greedierdb = MySQLdb.connect(passwd=mysqlpass, db=mysqldb, cursorclass = MySQLdb.cursors.SSCursor, connect_timeout=10)
greediercursor = greedierdb.cursor()

greediercursor.execute("SET interactive_timeout=3600")
greediercursor.execute("SET wait_timeout=3600")

greediercursor.execute("SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode, 'ERROR_FOR_DIVISION_BY_ZERO', ''))")

def getDateURL(dlc, pullDate):
    if (dlc == "scoresr"):
        dateURLFile = "datescoreurls-rep.txt"
    elif (dlc == "scoresabp"):
        dateURLFile = "datescoreurls-abp.txt"
    elif (dlc == "scoresab"):
        dateURLFile = "datescoreurls-ab.txt"
    with open(dateURLFile, 'r') as dateURLs:
        dateURLPairs = dateURLs.readlines()

    for dateURLPairString in dateURLPairs:
        dateURLPair = dateURLPairString.split(':')
        if dateURLPair[1].strip() == pullDate:
            return "https://steamcommunity.com/stats/250900/leaderboards/" + dateURLPair[0] + "/?xml=1"

    return ''

def to_little(val):
    little_hex = bytearray.fromhex(val)
    little_hex.reverse()

    return ''.join(format(x, '02x') for x in little_hex)

if (len(sys.argv)-1) != 2:
    print("Usage: " + sys.argv[0] + " <date, yyyymmdd>", file=sys.stderr)
    sys.exit(-1)

destTable = sys.argv[1]

if (destTable != "scoresr" and destTable != "scoresabp" and destTable != "scoresab"):
    print("Error: Invalid destination table!")
    sys.exit(-1)

pullDate = sys.argv[2]
dateURL = getDateURL(destTable, pullDate)

counter = 0
processedRecords = 0
while True:
    try:
        leaderboardPayload = requests.get(dateURL)
        leaderboard = xmltodict.parse(leaderboardPayload.content)
        break
    except Exception as e: 
        time.sleep(30)
        pass

totalRecords = int(leaderboard["response"]["totalLeaderboardEntries"])

greediercursor.execute("""SELECT steamid FROM profiles WHERE blacklisted=true""")

insertList = []
banList = []
steamIDList = []

if (leaderboard["response"]["resultCount"] == "0"):
    sys.exit(0)

while True:
    for leaderboardEntry in leaderboard["response"]["entries"]["entry"]:
        banned = False
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
            banned = True
            banList.append((int(leaderboardEntry["steamid"]), "Impossible time penalty %d on %s" % (timePenalty, pullDate)))

        if schwagBonus > 19150:
            banned = True
            banList.append((int(leaderboardEntry["steamid"]), "Impossible schwag bonus %d on %s" % (schwagBonus, pullDate)))

        scoreKey = leaderboardEntry['steamid'] + '.' + pullDate
        steamIDList.append(int(leaderboardEntry['steamid']))
        insertList.append((int(pullDate), scoreKey, int(leaderboardEntry["steamid"]), int(leaderboardEntry["rank"]), int(leaderboardEntry["score"]), stageBonus, explorationBonus, schwagBonus, rushBonus, bluebabyBonus, lambBonus, megasatanBonus, damagePenalty, timePenalty, itemPenalty, level, timeTaken, goal, leaderboardEntry["details"], shortenedLine, int(leaderboardEntry['rank']), int(leaderboardEntry["score"]), stageBonus, explorationBonus, schwagBonus, rushBonus, bluebabyBonus, lambBonus, megasatanBonus, damagePenalty, timePenalty, itemPenalty, level, timeTaken, goal, leaderboardEntry["details"], shortenedLine))

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
for record in insertList[:-1]: #[::-1]:
    recordWithDLC = list(record)
    recordWithDLC.pop(36)
    recordWithDLC.pop(19)
    recordWithDLC.pop(1)
    if destTable == "scoresab":
        recordWithDLC.insert(18, "ab")
        recordWithDLC.insert(37, "ab")
    elif destTable == "scoresabp":
        recordWithDLC.insert(18, "abp")
        recordWithDLC.insert(37, "abp")
    else:
        recordWithDLC.insert(18, "rep")
        recordWithDLC.insert(37, "rep")
    
    greediercursor.execute("""
        INSERT INTO
            """+destTable+"""
            (
                date,
                scorekey,
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
                shortenedline)
            VALUES(%s, %s, %s, %s, 0, 0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                shortenedline=%s
        """, record)
    
    greediercursor.execute("""
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
        """, recordWithDLC)


#### Rerank the current day's combined scores table.
greediercursor.execute("""
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
""", { 'today': pullDate })

greediercursor.execute("""
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

for profile in steamIDList:
    greediercursor.execute("""INSERT IGNORE INTO profiles (steamid, personaname) VALUES (%s, 'Unknown user')""", (int(profile),))

for profile in banList:
    greediercursor.execute("""INSERT INTO profiles (steamid, blacklisted, blacklisted_by, blacklisted_reason, blacklisted_date) VALUES(%s, true, 0, %s, TIMESTAMP(NOW())) ON DUPLICATE KEY UPDATE blacklisted=true, blacklisted_by=0, blacklisted_reason=%s""", (profile[0], profile[1], profile[1]))

greediercursor.execute("""UPDATE metadata SET activeplayercount=(SELECT COUNT(DISTINCT steamid) FROM """+destTable+""" WHERE scorerank<999999 AND scorerank>0 AND goal>0)""")
greediercursor.execute("""UPDATE metadata SET scorelinecount=(SELECT COUNT(scoreid) FROM scoresab)+(SELECT COUNT(scoreid) FROM scoresabp)+(SELECT COUNT(scoreid) FROM scoresr)""")
greedierdb.commit()
greedierdb.close()

sys.exit()
