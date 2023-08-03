from greedierbutt_flask import init_app

flask_app = init_app()
celery_app = flask_app.extensions["celery"]