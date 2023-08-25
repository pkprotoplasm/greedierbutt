"""Application entry point."""
from greedierbutt_flask import init_app, dbConn
from greedierbutt_flask.jobs.scores import scheduled_score_pull
from greedierbutt_flask.jobs.profiles import scheduled_profile_pull

from flask import g
from flask import request, session
from flask import render_template
from urllib.parse import urlparse
import re


# Generates UUIDs for 500 ISE pages and tags a log entry with them.
import uuid

import logging
logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger

app = init_app()
celery = app.extensions['celery']

@app.before_request
def open_cursor():
    g.cursor = dbConn.connection.cursor()

@app.before_request
def set_globals():
    g.dlc = get_dlc(urlparse(request.base_url).hostname)
    g.instance = get_instance(urlparse(request.base_url).hostname)
    g.domain = app.config.get("SESSION_COOKIE_DOMAIN")
    g.mod_list = get_mod_list()

@app.before_request
def mysql_charset():
    g.cursor.execute('CALL GetPendingReviews(%s)', [session.get('steamid', 00000)])
    g.pending_reviews = g.cursor.fetchall()

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'cursor'):
        g.cursor.close()

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title="N̸̢̛o̴͚͛ẗ̸͇ ̴̭͑F̷̤̅o̴̡̚u̴̺͝n̵͚͒d̶̤͘", message="Not sure what you were looking for, but it's not here..."), 404

@app.errorhandler(500)
def internal_server_error(e):
    error_uuid = uuid.uuid4()
    logger.error(f"{error_uuid}: {e}")
    return render_template("500.html", error_uuid=error_uuid), 500
        
def get_dlc(hostName):
    re_validator = re.compile(r'^[0-9a-zA-Z_\$]+$')
    
    dlc = "rep"
    if (hostName.split(".")[0] == "abp" or hostName.split(".")[0] == "ab") and re_validator.match(hostName.split(".")[0]):
        dlc = hostName.split(".")[0]
    return dlc

def get_instance(hostName):
    instance = "PROD"
    if "staging" in hostName:
        instance = "staging"
    return instance

def get_mod_list():
    g.cursor.execute("select steamid, personaname as player, avatar from profiles where moderator=true")

    return g.cursor.fetchall()

def get_admin_list():
    g.cursor.execute("select steamid, personaname as player, avatar from profiles where admin=true")

    return g.cursor.fetchall()

if __name__ == "__wsgi__":
    app.run(host="127.0.0.1")
