"""
__author__ = 'Slevin'
"""

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

from config import config

db = SQLAlchemy()
redis_store = FlaskRedis()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    redis_store.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
