class Config:
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

    SERVER_PORT = 5000

    SQLALCHEMY_DATABASE_URI = "sqlite:////Users/Thalles/Documents/programs/python/APIPortalCEFET/db/sqlite.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_EXPIRE = 10 * 60
