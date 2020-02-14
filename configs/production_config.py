from configs.config import Config
from os import environ


class ProductionConfig(Config):
    SERVER_IP = environ.get('SERVER_IP_PROD')
    SERVER_NAME = 'https://api-portal-cefet.herokuapp.com'
