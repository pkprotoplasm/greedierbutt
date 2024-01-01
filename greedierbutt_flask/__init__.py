import os

from flask import Flask
from flask import g
from flask_mysqldb import MySQL
from flask_caching import Cache
from flask_assets import Environment, Bundle

from celery import Celery
from celery_singleton import Singleton
from celery.schedules import crontab
from kombu import Exchange, Queue

from datetime import timedelta

dbConn = MySQL()
celery = Celery()
cache = Cache()
assets = Environment()

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
    

def init_app(test_config=None) -> Flask:

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.Config")
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    app.secret_key = app.config["SECRET_KEY"]
    app.config["SESSION_PERMANENT"] = True

    app.config.from_mapping(
        CELERY=dict(
            broker_url=app.config["CELERY_BROKER_URL"],
            result_backend=app.config["CELERY_RESULT_BACKEND"],
            task_ignore_result=True,
            broker_connection_retry_on_startup=True
        )
    )

    dbConn.init_app(app)
    celery_app = celery_init_app(app)

    assets.init_app(app)

    # Pull steam scores every 10 minutes.
    celery_app.add_periodic_task(timedelta(minutes=10), jobs.scores.scheduled_score_pull, name='10 minute score pull', priority=3)

    # Pull profiles for players active in the last 48 hours, every 60 minutes.
    celery_app.add_periodic_task(timedelta(minutes=60), jobs.profiles.scheduled_profile_pull, name='hourly profile pull', kwargs={'span': 'default'}, priority=3)
    
    ### Daily jobs - staggered by minute to properly queue
    # Pull the past 7 days for each dlc, daily at 11:15am UTC (15 minutes after daily changeover).
    celery_app.add_periodic_task(crontab(minute='15', hour='11'), jobs.scores.scheduled_daily_lookback, name='daily score lookback', priority=3)

    # Update score and time ranks on all score lines affected by the past day's bans, daily at 11:16am UTC (16 minutes after daily changeover).
    celery_app.add_periodic_task(crontab(minute='16', hour='11'), jobs.scores.scheduled_daily_rerank, name='daily banned rerank', priority=3)

    # Fetch player profiles every day at 11:16am UTC (16 minutes after daily changeover). This can overlap due to different tables.
    celery_app.add_periodic_task(crontab(minute='16', hour='11'), jobs.profiles.scheduled_profile_pull, name='daily profile pull', kwargs={'span': 'all'}, priority=3)

    # Calculate leaderboards every day at 11:17am UTC (17 minutes after daily changeover).
    celery_app.add_periodic_task(crontab(minute='17', hour='11'), jobs.scores.scheduled_top100_noaltf4, name='daily top100 recalculation', priority=3)

    cache.init_app(app)

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

        assets.append_path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'node_modules')))

        return app


def celery_init_app(app: Flask) -> Celery:
    app = app or init_app()

    class FlaskSingleton(Singleton):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                try:
                    return self.run(*args, **kwargs)
                except Exception as e:
                    self.release_lock(task_args=args, task_kwargs=kwargs)
                    return e
            
    celery_app = Celery(app.name, task_cls=FlaskSingleton)
    celery_app.config_from_object(app.config["CELERY"])

    celery_app.conf.broker_transport_options = {
        'priority_steps': list(range(3)),
        'sep': ':',
        'queue_order_strategy': 'priority'
    }

    celery_app.conf.task_queues = {
        Queue('default_jobs', Exchange('jobs'), routing_key='jobs.default'),
        Queue('score_jobs', Exchange('jobs'), routing_key='jobs.score'),
        Queue('profile_jobs', Exchange('jobs'), routing_key='jobs.profile')
    }

    celery_app.conf.task_default_queue = 'default_jobs'
    celery_app.conf.task_default_exchange_type = 'direct'
    celery_app.conf.task_default_routing_key = 'jobs.default'

    celery_app.conf.task_routes = {
        'jobs.scores.*': {
            'queue': 'score_jobs',
            'exchange': 'jobs',
            'priority': 3
        },
        'jobs.profiles.*': {
            'queue': 'profile_jobs',
            'exchange': 'jobs',
            'priority': 3
        }
    }

    celery_app.set_default()
    app.extensions["celery"] = celery_app

    celery_app.Task = FlaskSingleton

    return celery_app