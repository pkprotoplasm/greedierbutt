# Flask imports
from flask import Blueprint
from flask import current_app as app
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
from flask import session
from flask import g

# Application imports
from greedierbutt_flask import dbConn
from greedierbutt_flask.jobs.profiles import update_steam_profile

# General Python imports
from urllib.parse import urlparse
import requests

# Steam Login
from pysteamsignin.steamsignin import SteamSignIn

import logging
logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger


# Build blueprint
loginflow_bp = Blueprint(
    "loginflow_bp", __name__, template_folder="templates", static_folder="static"
)

@loginflow_bp.route("/login")
def initiate_login():
    session["redirect"] = request.headers.get("Referer")

    # If the user isn't already logged in, and the referer is local, redirect to Steam Sign-in.
    if not "steamid" in session.keys() and urlparse(request.headers.get("Referer")).hostname == urlparse(request.base_url).hostname:
        session.modified = True
        steamLogin = SteamSignIn()
        return steamLogin.RedirectUser(steamLogin.ConstructURL(str(f"{request.url_root}{url_for('loginflow_bp.login_callback')}")))
    else:
        # Mitigate malicious login farmers - if referer isn't local, kick back to the referring page.
        try:
            return redirect(request.headers.get("Referer"))
        except:
            return redirect(url_for('daily_bp.daily'))
    
@loginflow_bp.route("/logincallback")
def login_callback():
    # Validate Steam callback data.
    returnData = request.values

    steamLogin = SteamSignIn()
    steamID = steamLogin.ValidateResults(returnData)

    if steamID is not False:
        session.permanent = True
        # Set the steamid in session.
        session["steamid"] = steamID
        
        try:
            # Call the Steam API to get the rest of the player's profile information.
            r = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={app.config.get('STEAM_KEY')}&steamids={steamID}")
            steamJSON = r.json()['response']['players'][0]
            logger.info(r.json())
            logger.info(r.status_code)

            if r.status_code >= 400:
                raise Exception(f"API call failed for login_callback(). Status code: {r.status_code}")
            else:
                # Set additional necessary session variables for frontend.
                session["personaname"] = steamJSON["personaname"]
                session["avatar"] = steamJSON["avatar"]

                session.modified = True

                # Update the player's profile stored in our database.
                update_steam_profile.delay(steamid=steamID, personaname=steamJSON["personaname"], profileurl=steamJSON["profileurl"], avatar=steamJSON["avatar"], avatarmedium=steamJSON["avatarmedium"], avatarfull=steamJSON["avatarfull"])

        except Exception as e:
            g.cursor.execute("SELECT personaname, avatar FROM profiles WHERE steamid=%s LIMIT 1", [steamID])
            profileRow = g.cursor.fetchone()

            session["personaname"] = profileRow["personaname"]
            session["avatar"] = profileRow["avatar"]

            logger.warn(f"login_callback(): Exception: {e}")
        
        flash("Thanks for logging in!", "success")
    else:
        flash("Login failed. Please try logging in through Steam again.", "error")
    return redirect(session.get("redirect", url_for('daily_bp.daily')))

@loginflow_bp.route("/logout")
def logout():
    # Remove the variables from the session. Note: don't destroy the session entirely.
    session.pop("steamid", None)
    session.pop("personaname", None)
    session.pop("avatar", None)
    return redirect(request.headers.get("Referer"))