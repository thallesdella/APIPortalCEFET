from apicefet.controllers.profile import Profile

profile = Profile()
profile.blueprint.add_url_rule('', 'user.user', profile.perfilDados)
profile.blueprint.add_url_rule('/geral', 'user.geral', profile.perfilDadosGerais)
profile.blueprint.add_url_rule('/foto', 'user.photo', profile.perfilFoto)
