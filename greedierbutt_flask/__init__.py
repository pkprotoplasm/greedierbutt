import os

from flask import Flask
from flask import g
from flask import request
from flask_mysqldb import MySQL
from flask_caching import Cache

from celery import Celery, Task

import re
from datetime import timedelta

from config import Config

dbConn = MySQL()
cache = Cache()

# strptime filter for templates
def format_time_filter(seconds):
    try:
        rseconds = round(seconds)
        td = timedelta(seconds=round(rseconds, 2))
        microsecond = td.microseconds
        decisecond = int(round(microsecond/10000))
        return str(td).replace('.{:06d}'.format(microsecond), '.{:02d}'.format(decisecond))
    except:
        return '0:00:00'
    
# conditional layout filter for moderators
def is_moderator(steamid):
    try:
        result = g.mod_list[next((i for i, row in enumerate(g.mod_list) if row['steamid'] == int(steamid)), None)]
        return not(result == None)
    except:
        return False
    
# Starter celery_init_app code from Flask documentation.
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def init_app(test_config=None) -> Flask:

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.Config")
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    app.secret_key = app.config["SECRET_KEY"]
    app.config["SESSION_PERMANENT"] = True

    app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True
        )
    )

    dbConn.init_app(app)
    cache.init_app(app)
    celery_init_app(app)

    with app.app_context():
        app.jinja_env.filters['format_time'] = format_time_filter
        app.jinja_env.filters['is_moderator'] = is_moderator

        from .daily import daily
        from .loginflow import loginflow
        from .player import player
        from .score import score
        from .moderator import moderator

        app.config.update(
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE='None',
            PERMANENT_SESSION_LIFETIME = timedelta(days=90)
        )

        app.register_blueprint(daily.daily_bp)
        app.register_blueprint(loginflow.loginflow_bp)
        app.register_blueprint(player.player_bp)
        app.register_blueprint(score.score_bp)
        app.register_blueprint(moderator.moderator_bp)

        return app
