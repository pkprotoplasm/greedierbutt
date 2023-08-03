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

import logging
logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger

# Build blueprint
score_bp = Blueprint(
    "score_bp", __name__, template_folder="templates", static_folder="static"
)

# Outputs a formatted date string. "Monday April 1, 2023"
@app.template_filter()
def format_score_date(date_arg):
    dateobj = datetime.strptime(str(date_arg), "%Y%m%d")
    return dateobj.strftime("%a %b %d, %Y")

# Outputs a formatted short date string. "04/01/2023"
@app.template_filter()
def format_short_date(date_arg):
    dateobj = datetime.strptime(str(date_arg), "%Y%m%d")
    return dateobj.strftime("%m/%d/%Y")

# Outputs the header for the daily's goal bonus (e.g. Blue Baby, Lamb, Megasatan)
@app.template_filter()
def goal_bonus_header(row):
    try:
        if row['megasatan_bonus'] > 0:
            return "Mega Satan"
        elif row['lamb_bonus'] > 0:
            return "Lamb"
        elif row['bluebaby_bonus'] > 0:
            return "Blue Baby"
        else:
            return ""
    except:
        return ""

# Outputs the score for the daily's goal bonus (e.g. Blue Baby, Lamb, Megasatan)
@app.template_filter()
def goal_bonus(row):
    try:
        if row['megasatan_bonus'] > 0:
            return row['megasatan_bonus']
        elif row['lamb_bonus'] > 0:
            return row['lamb_bonus']
        elif row['bluebaby_bonus'] > 0:
            return row['bluebaby_bonus']
        else:
            return 0
    except:
        return 0

# Breaking change from gb-php: Player pages are only accessible via steam ID now.
@score_bp.route("/score/<int:scoreid>", strict_slashes=False)
def score(scoreid):
    startTime = datetime.now()

    daily_view = f"alldaily_scores_{g.dlc}" # get_dlc() is SQL safe
    if g.dlc == "abp":
        daily_table = "scoresabp"
    elif g.dlc == "ab":
        daily_table = "scoresab"
    else:
        daily_table = "scoresr"

    # Grab the requested score by ID.
    g.cursor.execute("CALL GetScore(%s, %s)", [g.dlc, scoreid])
    dbResult = g.cursor.fetchall()
    if len(dbResult) == 0:
        return render_template("404.html", title="Entry not found", message="Sorry, we couldn't find that entry!"), 404
    
    score = dbResult[0]

    # Display the page.
    return render_template("score.html", score=score)

@score_bp.route("/report/<int:scoreid>", strict_slashes=False, methods=['POST'])
def report(scoreid):
    # Try populating the report row.
    try:
        g.cursor.execute("INSERT INTO reports (scoreid, steamid, reporter, reason, dlc) VALUES (%s, %s, %s, %s, %s)", [scoreid, request.form['steamid'], session['steamid'], request.form['reason'], g.dlc])
        dbConn.connection.commit()
        flash(message="Thank you. Moderators will review your report soon.", category="success")
    except Exception as e:
        flash(message="Something went wrong. Try submitting your report again.", category="error")

    return redirect(url_for('score_bp.score', scoreid=scoreid))