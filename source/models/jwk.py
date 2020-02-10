from sqlalchemy import Column, Integer, String
from source.core.db import Db


class Jwk(Db.base()):
    _tablename__ = 'jwt_key'
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True)
    type = Column(String(10))
