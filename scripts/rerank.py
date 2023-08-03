#!/usr/bin/python3

import sys
import MySQLdb
import MySQLdb.cursors
import datetime
from os import path

sys.path.append(path.dirname(path.realpath(__file__)))

from config import Config

mysqlpass=Config.MYSQL_PASSWORD
mysqldb=Config.MYSQL_DB

greedierdb = MySQLdb.connect(passwd=mysqlpass, db=mysqldb, cursorclass = MySQLdb.cursors.SSCursor)
greediercursor = greedierdb.cursor()

greediercursor.execute("""UPDATE LOW_PRIORITY reports SET processed=true WHERE approved=true""")

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
""", { 'today': f"{datetime.date.today():%Y%m%d}" })

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

greediercursor.execute("""UPDATE LOW_PRIORITY metadata SET lastupdate=TIMESTAMP(NOW())""")

greedierdb.commit()
greedierdb.close()

sys.exit()
