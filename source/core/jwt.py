from source.models.jwk import Jwk as JwkModel
from json import dumps as json_encode
from json import loads as json_decode
from jwcrypto import jwt, jwk


class Jwt:
    def __init__(self, token=None):
        self._token = token

        if not JwkModel.query.count():
            self.__create_key()
        else:
            self.__get_key()

    def create_token(self, data):
        enc_jwt = jwt.JWT(header={"alg": "HS256"}, claims=data)
        enc_jwt.make_signed_token(json_encode(self.__key))
        return enc_jwt.serialize()

    def get_token_data(self):
        key = jwk.JWK(**self.__key)
        dec_jwt = jwt.JWT().deserialize(jwt=self._token, key=key)
        return dec_jwt.claim

    def validate_token(self):
        key = jwk.JWK(**self.__key)
        dec_jwt = jwt.JWT().deserialize(jwt=self._token, key=key)
        return dec_jwt.token.is_valid

    def __create_key(self):
        jwk_key = jwk.JWK(generate='oct', size=256)
        self.__key = json_decode(jwk_key.export())

        jwk_model = JwkModel(self.__key['k'], self.__key['kty'])
        jwk_model.add()
        jwk_model.commit()
        return

    def __get_key(self):
        pass
