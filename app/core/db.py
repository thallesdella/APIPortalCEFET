from flask import current_app, g
import sqlite3


class Db:
    def __init__(self):
        if 'db' not in g:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        self.db = g.db

    def get_db(self):
        return self.db

    @staticmethod
    def close_db(e=None):
        db_handle = g.pop('db', None)

        if db_handle is not None:
            db_handle.close()
