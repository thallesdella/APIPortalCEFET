from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Db:
    @staticmethod
    def base():
        base = declarative_base()
        base.query = Db.__db_session().query_property()
        return base

    @staticmethod
    def create_db():
        Db.base().metadata.create_all(bind=Db.__engine())

    @staticmethod
    def close_db():
        Db.__db_session().remove()
        return

    @staticmethod
    def __engine():
        return create_engine(current_app, convert_unicode=True)

    @staticmethod
    def __db_session():
        return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=Db.__engine()))
