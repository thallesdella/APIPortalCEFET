from apicefet.models.jwk import db, Jwk as JwkModel
from itsdangerous import TimedJSONWebSignatureSerializer
from os import urandom


class Jwt:
    def __init__(self):
        if not JwkModel.query.count():
            self.__create_key()
        else:
            self.__get_key()

    def create_token(self, data):
        jwt = TimedJSONWebSignatureSerializer(self.__key, expires_in=600)
        return jwt.dumps(data)

    def get_token_data(self, token):
        jwt = TimedJSONWebSignatureSerializer(self.__key, expires_in=600)
        return jwt.loads(token)

    def __create_key(self):
        self.__key = urandom(24).hex()

        jwk_model = JwkModel(self.__key)

        db.session.add(jwk_model)
        db.session.commit()
        return

    def __get_key(self):
        pass
