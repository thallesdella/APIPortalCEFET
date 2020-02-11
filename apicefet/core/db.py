from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Db:
    def __init__(self, current_app):
        self.current_app = current_app

    @property
    def base(self):
        base = declarative_base()
        base.query = self.__db_session().query_property()
        return base

    def create_db(self):
        # import models to make sure they are available
        # when creating the db
        import apicefet.models.jwk

        self.base.metadata.create_all(bind=self.__engine())
        return

    def close_db(self):
        self.__db_session().remove()
        return

    def __engine(self):
        return create_engine(self.current_app.config['DATABASE_URI'], convert_unicode=True)

    def __db_session(self):
        return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.__engine()))
