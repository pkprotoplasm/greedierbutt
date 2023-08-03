#!/usr/bin/python3

import sys
import MySQLdb
import MySQLdb.cursors
import datetime

from os import path

sys.path.append(path.dirname(path.realpath(__file__)))

from config import Config

mysqlpass=Config.MYSQL_WRITE_PASSWORD
mysqldb=Config.MYSQL_DB

if (len(sys.argv)-1) == 1:
    startDate = sys.argv[1]
else:
    print("Usage: " + sys.argv[0] + " <start date, yyyymmdd>", file=sys.stderr)
    sys.exit(-1)

greedierdb = MySQLdb.connect(passwd=mysqlpass, db=mysqldb, cursorclass = MySQLdb.cursors.SSCursor)
greediercursor = greedierdb.cursor()

### Repentance
greediercursor.execute("""delete from toprankingsr""")
greediercursor.execute("""
INSERT INTO
    toprankingsr
WITH
    entries AS (
        SELECT
            steamid,
            count(scoreid) as entrycount
        FROM
            scores
        WHERE
            date>=%(date)s and
            date<%(today)s and
            score>0 and
            time>0 and
            dlc="rep"
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
            date>=%(date)s and
            date<%(today)s and
            score=0 and
            time=0 and
            dlc="rep"
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
                s.date>=%(date)s AND
                s.date<%(today)s AND
                s.score>0 AND
                s.time>0 AND
                s.dlc="rep"
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
""", { 'date': startDate, 'today': f"{datetime.date.today():%Y%m%d}" })

### Afterbirth+
greediercursor.execute("""delete from toprankingsabp""")
greediercursor.execute("""
INSERT INTO
    toprankingsabp
WITH
    entries AS (
        SELECT
            steamid,
            count(scoreid) as entrycount
        FROM
            scores
        WHERE
            date>=%(date)s and
            date<%(today)s and
            score>0 and
            time>0 and
            dlc="abp"
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
            date>=%(date)s and
            date<%(today)s and
            score=0 and
            time=0 and
            dlc="abp"
        GROUP BY
            steamid
    ),
    averages AS (
        SELECT
            scoresabp.steamid as steamid,
            avg(scoresabp.scorerank) AS scorerank,
            avg(scoresabp.timerank) AS timerank,
            avg(scoresabp.scorepercentile) AS scorepercentile,
            avg(scoresabp.timepercentile) AS timepercentile
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
                s.date>=%(date)s AND
                s.date<%(today)s AND
                s.score>0 AND
                s.time>0 AND
                s.dlc="abp"
            ) AS scoresabp
        GROUP BY
            scoresabp.steamid
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
""", { 'date': startDate, 'today': f"{datetime.date.today():%Y%m%d}" })


### Afterbirth
greediercursor.execute("""delete from toprankingsab""")
greediercursor.execute("""
INSERT INTO
    toprankingsab
WITH
    entries AS (
        SELECT
            steamid,
            count(scoreid) as entrycount
        FROM
            scores
        WHERE
            date>=%(date)s and
            date<%(today)s and
            score>0 and
            time>0 and
            dlc="ab"
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
            date>=%(date)s and
            date<%(today)s and
            score=0 and
            time=0 and
            dlc="ab"
        GROUP BY
            steamid
    ),
    averages AS (
        SELECT
            scoresab.steamid as steamid,
            avg(scoresab.scorerank) AS scorerank,
            avg(scoresab.timerank) AS timerank,
            avg(scoresab.scorepercentile) AS scorepercentile,
            avg(scoresab.timepercentile) AS timepercentile
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
                s.date>=%(date)s AND
                s.date<%(today)s AND
                s.score>0 AND
                s.time>0 AND
                s.dlc="ab"
            ) AS scoresab
        GROUP BY
            scoresab.steamid
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
""", { 'date': startDate, 'today': f"{datetime.date.today():%Y%m%d}" })



greediercursor.execute("""UPDATE LOW_PRIORITY metadata SET lastupdate=TIMESTAMP(NOW())""")

greedierdb.commit()
greedierdb.close()

sys.exit()
