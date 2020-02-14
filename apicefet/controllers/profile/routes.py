from apicefet.controllers.profile import Profile

profile = Profile()
profile.blueprint.add_url_rule('', 'user', profile.perfilDados)
profile.blueprint.add_url_rule('/geral', 'geral', profile.perfilDadosGerais)
profile.blueprint.add_url_rule('/foto', 'photo', profile.perfilFoto)
