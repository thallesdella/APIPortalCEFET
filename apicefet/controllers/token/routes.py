from apicefet.controllers.token import Token

token = Token()
token.blueprint.add_url_rule('/<string:user>/<string:passwd>', 'auth.user', token.get_token)
