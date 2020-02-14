from apicefet import db


class Jwk(db.Model):
    db.__tablename__ = 'jwt_secret'

    id = db.Column(db.Integer, primary_key=True)
    secret = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, secret):
        self.secret = secret
