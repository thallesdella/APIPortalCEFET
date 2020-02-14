from apicefet.controllers.reports import Report

report = Report()
report.blueprint.add_url_rule('', 'list', report.lista_relatorios)
report.blueprint.add_url_rule('/<path:url>', 'generate', report.geraRelatorio)
