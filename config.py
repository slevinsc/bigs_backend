__author__ = 'Slevin'
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'NNuletCPFXdAmeS^g5dqrBrayjvTtFHO'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql://root:000000@localhost/bigs_dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    REDIS_URL = "redis://localhost:6379/0"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:000000@localhost/bigs_test"
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:000000@localhost/bigs"


config = {
    'default': DevelopmentConfig,
    'prod': ProductionConfig,
    'testing': TestingConfig
}
