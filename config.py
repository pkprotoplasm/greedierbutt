"""Class-based Flask app configuration."""
from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Configuration from environment variables."""

    FLASK_ENV = environ.get("FLASK_DEBUG")
    FLASK_APP = "wsgi.py"

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = True

    MYSQL_DB = environ.get("MYSQL_DB")
    MYSQL_USER = environ.get("MYSQL_USER")
    MYSQL_PASSWORD = environ.get("MYSQL_PASSWORD")

    CACHE_TYPE = environ.get("CACHE_TYPE")
    CACHE_DEFAULT_TIMEOUT = environ.get("CACHE_DEFAULT_TIMEOUT")

    SESSION_TYPE = environ.get("SESSION_TYPE")
    SESSION_COOKIE_DOMAIN = environ.get("SESSION_COOKIE_DOMAIN")

    SECRET_KEY = environ.get("SECRET_KEY")

    STEAM_KEY = environ.get("STEAM_KEY")