from configs.config import Config
from os import environ


class DevelopmentConfig(Config):
    SERVER_IP = environ.get('SERVER_IP_DEV')
    SERVER_NAME = 'localhost'

    FLASK_ENV = 'development'
    TESTING = True
