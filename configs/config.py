from os import environ


class Config:
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
