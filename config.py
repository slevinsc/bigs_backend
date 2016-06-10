__author__ = 'Slevin'


class Config:
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'NNuletCPFXdAmeS^g5dqrBrayjvTtFHO'
    SQLALCHEMY_DATABASE_URI = "mysql://root:000000@localhost/test"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    REDIS_URL = "redis://localhost:6379/0"


config = {
    'default': DevelopmentConfig
}
