from apicefet.models.jwk import Jwk as JwkModel
from itsdangerous import TimedJSONWebSignatureSerializer
from apicefet import create_app as app
from os import urandom


class Jwt:
    def __init__(self):
        if not JwkModel().count():
            self.__create_key()
        else:
            self.__get_key()

    def create_token(self, data):
        jwt = TimedJSONWebSignatureSerializer(self.__key, expires_in=app().config['TOKEN_EXPIRE'])
        return jwt.dumps(data)

    def get_token_data(self, token):
        jwt = TimedJSONWebSignatureSerializer(self.__key, expires_in=app().config['TOKEN_EXPIRE'])
        return jwt.loads(token)

    def __create_key(self):
        self.__key = urandom(24).hex()
        JwkModel().bootstrap(self.__key)
        return

    def __get_key(self):
        table_data = JwkModel().dumps()
        self.__key = table_data[0]['secret']
        return
