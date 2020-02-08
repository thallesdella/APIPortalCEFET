from flask import Flask, jsonify

from controllers.auth import Auth as auth
from controllers.profile import Profile as profile
from controllers.report import Report as report
from controllers.schedule import Schedule as schedule

import os

app = Flask(__name__)

auth.blueprint.add_url_rule('', 'auth.user', auth.autenticacao(), methods=['POST'])
app.register_blueprint(auth.blueprint, url_prefix='/autenticacao')

profile.blueprint.add_url_rule('', 'user.user', profile.perfilDados())
profile.blueprint.add_url_rule('/geral', 'user.geral', profile.perfilDadosGerais())
profile.blueprint.add_url_rule('/foto', 'user.photo', profile.perfilFoto())
app.register_blueprint(profile.blueprint, url_prefix='/perfil')

report.blueprint.add_url_rule('', 'report.list', report.lista_relatorios())
report.blueprint.add_url_rule('/pdf', 'report.generate', report.geraRelatorio())
app.register_blueprint(report.blueprint, url_prefix='/relatorios')

schedule.blueprint.add_url_rule('', 'schedule.time', schedule.horarios())
app.register_blueprint(schedule.blueprint, url_prefix='/horarios')


@app.errorhandler(404)
def respond404(error):
    return jsonify({
        "code": 404,
        "error": "Nao encontrado"
    })


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)  # para prod, ative aqui!
    # app.run(debug=True, host='127.0.0.1', port=port)  # para dev, ative aqui!
