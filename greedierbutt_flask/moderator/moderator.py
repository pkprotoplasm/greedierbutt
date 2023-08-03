# Flask imports
from flask import abort
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
from greedierbutt_flask import cache, dbConn, format_time_filter

# General Python imports
from urllib.parse import urlparse
from datetime import date, datetime, timedelta

import logging
logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger

# Build blueprint
moderator_bp = Blueprint(
    "moderator_bp", __name__, template_folder="templates", static_folder="static"
)

def is_moderator(steamid):
    try:
        result = g.mod_list[next((i for i, row in enumerate(g.mod_list) if row['steamid'] == int(steamid)), None)]
        return not(result == None)
    except:
        return False

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

# Adds a formatted time element to report rows.
@app.template_filter()
def json_friendly_report(reports):
    try:
        formattedReports = []
        for report in reports:
            report['formatted_time'] = format_time_filter(int(report['time'])/30)
            report['formatted_date'] = format_short_date(report['scoredate'])

            report['steamid'] = str(report['steamid'])
            report['reporterid'] = str(report['reporterid'])

            report['form_action'] = url_for('moderator_bp.moderator_review', reportid=report['reportid'])
            report['reporter_link'] = url_for('player_bp.player', steamid=report['reporterid'])
            report['player_link'] = url_for('player_bp.player', steamid=report['steamid'], historyView="full")
            report['daily_link'] = url_for('daily_bp.daily', datearg=report['scoredate'], rankby='scores', arg3=report['steamid'])
            formattedReports.append(report)
        return formattedReports
    except:
        return []

@app.template_filter()
def mod_links(mod_list):
    try:
        mod_links = []

        for moderator in mod_list:
            mod_links.append(f'<a href="{url_for("player_bp.player", steamid=moderator["steamid"])}" title={moderator["player"]}>{moderator["player"]}</a>')
        return ', '.join(mod_links)
    except:
        return ''

@moderator_bp.route("/moderator", strict_slashes=False)
def moderator():
    try:
        # Access control
        if not is_moderator(session.get('steamid')):
            return render_template("403.html", title="Moderators Only", message="Only moderators can access this page."), 403

        return render_template('moderator.html', pendingReviews=g.pending_reviews)
    except Exception as e:
        abort(500, e)


# Breaking change from gb-php: Player pages are only accessible via steam ID now.
@moderator_bp.route("/moderator/review/<int:reportid>", strict_slashes=False, methods=['POST'])
def moderator_review(reportid):
    try:
        # Access control
        if not is_moderator(session.get('steamid')):
                return render_template("403.html", title="Moderators Only", message="Only moderators can access this page."), 403

        approved = 0
        if request.form['action'] == "accept":
            approved = 1

            # Set the player profile to blacklisted
            g.cursor.execute('UPDATE profiles AS p, reports AS r SET p.blacklisted=1, p.blacklisted_date=NOW(), p.blacklisted_by=%s, p.blacklisted_reason=%s WHERE p.steamid=r.steamid AND r.reportid=%s', [session.get('steamid'), request.form['reason'], reportid])

            # Set the score ranks to 999999
            g.cursor.execute('UPDATE scores AS s, reports AS r SET s.scorerank=999999, s.timerank=999999 WHERE s.steamid=r.steamid AND r.reportid=%s', [reportid])

        # Update the reports table.
        g.cursor.execute('UPDATE reports SET approved=%s, reviewer=%s, response=%s, processed=false WHERE reportid=%s', [approved, session.get('steamid'), request.form['reason'], reportid])

        g.cursor.close()
        dbConn.connection.commit()

        # Go back to the moderator page.
        return redirect(url_for('moderator_bp.moderator'))

    except Exception as e:
        abort(500, e)