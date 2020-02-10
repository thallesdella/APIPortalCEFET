from source.configs.config import Config


class DevelopmentConfig(Config):
    DEBUG = True

    DATABASE_URI = '/path/to/database.db'
