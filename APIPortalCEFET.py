from flask import Flask, json
from werkzeug.exceptions import HTTPException

from controllers.auth import Auth
from controllers.profile import Profile
from controllers.report import Report
from controllers.schedule import Schedule

import os

app = Flask(__name__)

Auth.blueprint.add_url_rule('/<string:user>/<string:passwd>', 'auth.user', Auth.autenticacao, methods=['POST'])
app.register_blueprint(Auth.blueprint, url_prefix='/autenticacao')

Profile.blueprint.add_url_rule('', 'user.user', Profile.perfilDados)
Profile.blueprint.add_url_rule('/geral', 'user.geral', Profile.perfilDadosGerais)
Profile.blueprint.add_url_rule('/foto', 'user.photo', Profile.perfilFoto)
app.register_blueprint(Profile.blueprint, url_prefix='/perfil')

Report.blueprint.add_url_rule('', 'report.list', Report.lista_relatorios)
Report.blueprint.add_url_rule('/<path:url>', 'report.generate', Report.geraRelatorio)
app.register_blueprint(Report.blueprint, url_prefix='/relatorios')

Schedule.blueprint.add_url_rule('', 'schedule.time', Schedule.horarios)
app.register_blueprint(Schedule.blueprint, url_prefix='/horarios')


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "error": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)  # para prod, ative aqui!
    # app.run(debug=True, host='127.0.0.1', port=port)  # para dev, ative aqui!
