from os import environ


class Config:
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

    SERVER_PORT = environ.get('SERVER_PORT')
    SERVER_NAME = environ.get('SERVER_NAME')

    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
