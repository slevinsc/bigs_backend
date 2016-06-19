__author__ = 'Slevin'
import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'NNuletCPFXdAmeS^g5dqrBrayjvTtFHO'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    # SQLALCHEMY_DATABASE_URI = "mysql://root:000000@localhost/bigs_dev"
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'data-dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    REDIS_URL = "redis://192.168.3.20:6379/0"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI ='sqlite:///'+os.path.join(basedir,'data-test.sqlite')
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REDIS_URL = "redis://192.168.3.20:6379/1"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'default': DevelopmentConfig,
    'prod': ProductionConfig,
    'testing': TestingConfig
}
