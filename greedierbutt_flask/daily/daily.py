# Flask imports
from flask import Blueprint
from flask import current_app as app
from flask import redirect
from flask import request
from flask import flash
from flask import render_template
from flask import url_for
from flask import session
from flask import g
from flask_paginate import Pagination

# Application imports
from greedierbutt_flask import cache, dbConn

# General Python imports
from urllib.parse import urlparse
from datetime import date, datetime, timedelta
from math import floor

# Pandas - to filter results
import pandas

import logging
logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger

def get_daily_goal(datearg):
    try:
        g.cursor.execute(f"SELECT goal FROM scores WHERE date=%s AND goal BETWEEN 2 AND 8 AND dlc=%s GROUP BY goal ORDER BY COUNT(goal) DESC LIMIT 1", [datearg, g.dlc])
        row = g.cursor.fetchall()[0]
        if row["goal"] == 2:
            return "Mom"
        elif row["goal"] == 3:
            return "It Lives / Mom's Heart"
        if row["goal"] == 4:
            return "Satan"
        if row["goal"] == 5:
            return "Isaac"
        if row["goal"] == 6:
            return "The Lamb"
        if row["goal"] == 7:
            return "???"
        if row["goal"] == 8:
            return "Mega Satan"
        else:
            return "Unknown"
    except:
        return "Unknown"

# Build blueprint
daily_bp = Blueprint(
    "daily_bp", __name__, template_folder="templates", static_folder="static"
)

@app.template_filter()
def date_add(dateArg, dayCount):
    return (dateArg + timedelta(days=dayCount))

@app.template_filter()
def get_badges(row):
    badges = []
    badgeMarkup = []

    if row['damage_penalty'] == 0 and row['level'] > 1:
        badges.append({'name': 'Mr. Clean', 'title': 'Took no hits!', 'class': 'success'})
    
    if row['exploration_bonus'] > 1000000:
        badges.append({'name': 'Marco Polo', 'title': 'Crazy high exploration bonus', 'class': 'info'})

    if row['score'] == 42069 or row['score'] == 69420 or row['score'] == 690420 or row['score'] == 666999 or row['score'] == 1666999:
        badges.append({'name': "Dave's Not Here", 'title': f'Funny number in score {row["score"]}', 'class': 'success'})

    if row['scorerank'] == 69 and row['timerank'] == 69:
        badges.append({'name': "Nicee!", 'title': 'Score AND Time rank of 69!!', 'class': 'success'})
    elif row['scorerank'] == 69:
        badges.append({'name': "Nice", 'title': 'Score rank of 69', 'class': 'success'})
    elif row['timerank'] == 69:
        badges.append({'name': "Nice", 'title': 'Time rank of 69', 'class': 'success'})

    if row['score'] == 5318008:
        badges.append({'name': '(.)(.)', 'title': 'Sexy score', 'class': 'success'})

    if row['time'] > (60 * 60 * 30): # Over an hour
        badges.append({'name': "Slow Mode", 'title': 'Took over an hour to finish', 'class': 'warning'})

    if not row['hits_taken'] == None and row['hits_taken'] > 50:
        badges.append({'name': "Punching Bag", 'title': f'Took a beating ({row["hits_taken"]} hits taken)', 'class': 'success'})

    if row['goal'] == 1:
        badges.append({'name': 'Today I Died', 'title': "Couldn't survive this run", 'class': 'danger'})

    for badge in badges:
        badgeMarkup.append(f'<span class="badge bg-{badge["class"]}" data-bs-toggle="tooltip" title="{badge["title"]}">{badge["name"]}</span>')

    return '\n'.join(badgeMarkup)

# arg3 is either a steam ID, player profile name, or page number
@daily_bp.route("/")
@daily_bp.route("/daily", strict_slashes=False)
@daily_bp.route("/daily/<int:datearg>", strict_slashes=False)
@daily_bp.route("/daily/<int:datearg>/<string:rankby>", strict_slashes=False)
@daily_bp.route("/daily/<int:datearg>/<string:rankby>/<string:arg3>")
def daily(datearg="0", rankby="scores", arg3="1"):

    startTime = datetime.now()

    # Determine today's date, which is 10 hours behind UTC for the purposes of Isaac bookkeeping.
    today = (datetime.utcnow() - timedelta(hours=10))

    # Hard-coded page length (for now)
    page_length=20

    # Parse date argument from URL (if it exists)
    try:
        date_given = datetime.strptime(f"{datearg}", '%Y%m%d')
    except:
        date_given = datetime.utcnow() - timedelta(hours=10)
        datearg = date_given.strftime('%Y%m%d')

    player = None
    page = None

    # arg3 is a Steam ID
    if len(arg3) == 17 and arg3.isdigit():
        player = int(arg3)
    # arg3 is a page number
    elif arg3.isdigit():
        page = int(arg3)

    # How we'll sort the scores
    if rankby == "times":
        orderBy = "timerank"
    else:
        orderBy = "scorerank"

    # Get the daily goal.
    if cache.has(f"goal_{datearg}"):
        goal = cache.get(f"goal{datearg}")
    else:
        goal = get_daily_goal(datearg)
        cache.set(f"goal{datearg}", goal, timeout=60)

    # Populate the full score list for the day. We'll paginate the results later. This allows caching for all pages.
    cacheKey = f"{g.dlc}/daily/{datearg}/{rankby}"
    if cache.has(cacheKey):
        rows = cache.get(cacheKey)
    else:                
        g.cursor.execute(f"SELECT * FROM scores_ranked WHERE date=%s AND dlc=%s ORDER BY {'timerow' if orderBy == 'timerank' else 'scorerow'} ASC", [datearg, g.dlc])
        rows = g.cursor.fetchall()
        cache.set(cacheKey, rows, timeout=60)

    # If arg3 was a steam ID, determine the page number it appears on & navigate to it. If it's not found, go to page 1.
    try:
        playerResult = rows[next((i for i, row in enumerate(rows) if row['steamid'] == int(player)), None)]

        page = floor(playerResult["timerow" if orderBy == "timerank" else "scorerow"] / page_length)+1
    except Exception as e:
        player = None
        if page == None:
            page = 1

    # If the user is logged in, get their result for the requested date, if it exists.
    try:
        userResult = rows[next((i for i, row in enumerate(rows) if row['steamid'] == int(session.get('steamid'))), None)]
    except Exception as e:
        userResult = None

    # Pagination for the results.
    pagination = Pagination(page=page, per_page=page_length, href=f"/daily/{datearg}/{rankby}/{{0}}", total=len(rows), search=False, record_name="scores", css_framework="bootstrap5", bs_version="5", link_size="sm", link_alignment="center", inner_window=1, outer_window=1)
    endTime = datetime.now()

    # Display the page.
    return render_template("daily.html", date=date_given, score_rows=rows[(page-1)*page_length:page*page_length], pagination=pagination, load_time=endTime-startTime, orderBy=orderBy, goal=goal, player=player, today=today, userResult=userResult)

@daily_bp.route("/top")
@daily_bp.route("/top/<string:leaderboard>", strict_slashes=False)
@daily_bp.route("/top/<string:leaderboard>/<string:sort>", strict_slashes=False)
def top(leaderboard="100", sort="scores"):

    try:
        # Safely default to the top-100 (non-alt F4) leaderboard.
        if leaderboard == "altf4":
            leaderboard = "altf4"
            lb_header_text = "Top 100 Alt F4"
        else:
            leaderboard = "100"
            lb_header_text = "Top 100 No-Alt F4"

        # Database views are provided in the backend for the various leaderboards.
        lb_view = f"lb_{leaderboard}_{g.dlc}" # get_dlc() is SQL safe

        # Default order is by scores, safely switch to times upon user request.
        orderBy = "scorerank"
        if sort == "times":
            orderBy = "timerank"

        # Fetch the data.
        g.cursor.execute(f"SELECT * FROM {lb_view} ORDER BY {orderBy} ASC LIMIT 100")
        results = g.cursor.fetchall()

        # Render the page.
        return render_template("top.html", leaderboard=leaderboard, results=results, sort=sort, orderBy=orderBy, lb_header_text=lb_header_text)
    except Exception as e:
        return render_template("404.html"), 404