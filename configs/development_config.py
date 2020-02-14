from configs.config import Config
from os import environ


class DevelopmentConfig(Config):
    SERVER_IP = '127.0.0.1'
    SERVER_NAME = 'http://localhost'

    FLASK_ENV = 'development'
    TESTING = True
