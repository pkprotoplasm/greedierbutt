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

# Pandas - for easy dictionary math.
import pandas

import logging
logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger

# Build blueprint
player_bp = Blueprint(
    "player_bp", __name__, template_folder="templates", static_folder="static"
)

@app.template_filter()
def format_streak_date(date_arg):
    dateobj = datetime.strptime(str(date_arg), "%Y%m%d")
    return dateobj.strftime("%a %b %d, %Y")

@app.template_filter()
def avg_dict_value(dict_object, element_name):
    # Convert dictionary to DataFrame
    dictDataFrame = pandas.DataFrame(dict_object)

    #Calculate the average (mathematical mean)
    return dictDataFrame[element_name].mean()

@app.template_filter()
def filter_runs(dict_object):
    try:
        # Convert dictionary to DataFrame
        dictDataFrame = pandas.DataFrame(dict_object)

        # Filter dictionary to exclude items with level=0
        return dictDataFrame[dictDataFrame['level'] > 0]
    except:
        return []

# Breaking change from gb-php: Player pages are only accessible via steam ID now.
@player_bp.route("/player/<int:steamid>", strict_slashes=False)
@player_bp.route("/player/<int:steamid>/<string:historyView>")
def player(steamid, historyView="none"):
    startTime = datetime.now()

    daily_view = f"alldaily_scores_{g.dlc}" # get_dlc() is SQL safe
    if g.dlc == "abp":
        daily_table = "scoresabp"
    elif g.dlc == "ab":
        daily_table = "scoresab"
    else:
        daily_table = "scoresr"

    # Check for cached player page. Fetch if there's no cached version.
    cacheKeyProfile = f"{g.dlc}/player/{steamid}/profile"
    cacheKeyRecentRuns = f"{g.dlc}/player/{steamid}/recentruns"
    cacheKeyRunHistory = f"{g.dlc}/player/{steamid}/run_history"
    try:
        dbResultProfile = cache.get(cacheKeyProfile)
        dbResultRuns = cache.get(cacheKeyRecentRuns)
        if dbResultProfile == None or dbResultRuns == None:
            raise TypeError("No cached profile information")        
    except:
        # Fetch the player's profile. Cache it once fetched.
        g.cursor.execute("CALL GetPlayerProfile(%s, %s)", [g.dlc, steamid])
        dbResultProfile = g.cursor.fetchall()
        cache.set(cacheKeyProfile, dbResultProfile, timeout=60)

        # Fetch the player's most recent runs. Currently hardcoded to a maximum of 10.
        g.cursor.execute("CALL GetPlayerRecentRuns(%s, %s, %s)", [g.dlc, steamid, 10])
        dbResultRuns = g.cursor.fetchall()
        cache.set(cacheKeyRecentRuns, dbResultRuns, timeout=60)

    # Fetch the player's full run history if requested.
    if historyView == "full":
        dbResultRunHistory = cache.get(cacheKeyRunHistory)
        if dbResultRunHistory == None:
            g.cursor.execute("SELECT * FROM score_history WHERE steamid=%s AND dlc=%s", [steamid, g.dlc])
            dbResultRunHistory = g.cursor.fetchall()
            cache.set(cacheKeyRunHistory, dbResultRunHistory, timeout=60)
    else:
        dbResultRunHistory = None

    # TODO: Handle profiles that don't have a ranked result yet - players that have played today's daily only.
    if len(dbResultProfile) == 0:
        return render_template("404.html", title="Player not found", message="Sorry, we couldn't find that player!"), 404
    
    profile = dbResultProfile[0]

    # Display the page.
    return render_template("player.html", load_time=(datetime.now()-startTime), profile=profile, recentruns=dbResultRuns, run_history=dbResultRunHistory, historyView=historyView)

@player_bp.route("/search", strict_slashes=False, methods=['GET', 'POST'])
def search():
    try:
        # Determine which table to search on. This is used on a join to the profiles table to determine how active matching players are.
        if g.dlc == "abp":
            daily_table = "scoresabp"
        elif g.dlc == "ab":
            daily_table = "scoresab"
        else:
            daily_table = "scoresr"

        # Call prepared database statement depending on which type of input was given.
        if len(request.form['player']) == 17 and request.form['player'].isdigit():
            g.cursor.execute("CALL SearchPlayersBySteamID(%s, %s)", [daily_table, request.form['player']])
        elif len(request.form['player']) > 2:
            g.cursor.execute("CALL SearchPlayersByName(%s, %s)", [daily_table, request.form['player']])
        else:
            flash('Please enter at least three characters in the search box.', 'error')
        results = g.cursor.fetchall()
    except Exception as e:
        results=None

    try:
        return render_template("search.html", query=request.form['player'], results=results)
    except:
        return redirect(url_for("daily_bp.daily"))