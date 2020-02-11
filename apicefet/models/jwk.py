from sqlalchemy import Column, Integer, String
from apicefet import db


class Jwk(db.Model):
    _tablename__ = 'jwt_key'
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    type = Column(String(10), nullable=False)

    def __init__(self, key, type):
        self.key = key
        self.type = type
