from flask import Flask, json
from werkzeug.exceptions import HTTPException

from source.configs.development_config import DevelopmentConfig as Configs  # para prod, ative aqui!

from source.core.db import Db

from source.controllers.token import Token
from source.controllers.profile import Profile
from source.controllers.report import Report
from source.controllers.schedule import Schedule

import os

app = Flask(__name__)

app.config.from_object(Configs)
app.teardown_appcontext(Db.close_db)

token = Token()
token.blueprint.add_url_rule('/<string:user>/<string:passwd>', 'auth.user', token.get_token)

app.register_blueprint(token.blueprint, url_prefix='/token')

profile = Profile()
profile.blueprint.add_url_rule('', 'user.user', profile.perfilDados)
profile.blueprint.add_url_rule('/geral', 'user.geral', profile.perfilDadosGerais)
profile.blueprint.add_url_rule('/foto', 'user.photo', profile.perfilFoto)

app.register_blueprint(profile.blueprint, url_prefix='/perfil')

report = Report()
report.blueprint.add_url_rule('', 'report.list', report.lista_relatorios)
report.blueprint.add_url_rule('/<path:url>', 'report.generate', report.geraRelatorio)

app.register_blueprint(report.blueprint, url_prefix='/relatorios')

schedule = Schedule()
schedule.blueprint.add_url_rule('', 'schedule.time', schedule.horarios)
app.register_blueprint(schedule.blueprint, url_prefix='/horarios')


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
    port = int(os.environ.get('PORT', app.config['SERVER_PORT']))
    app.run(debug=app.config['DEBUG'], host=app.config['SERVER_IP'], port=port)
