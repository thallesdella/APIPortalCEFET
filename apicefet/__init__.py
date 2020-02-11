from flask import Flask, json
from werkzeug.exceptions import HTTPException

from apicefet.core.db import Db

from apicefet.controllers.token.token import Token
from apicefet.controllers.profile.profile import Profile
from apicefet.controllers.reports.report import Report
from apicefet.controllers.schedule.schedule import Schedule


def create_app(env):
    app = Flask(__name__)

    if env == 'production':
        from configs.production_config import ProductionConfig as Config
    else:
        from configs.development_config import DevelopmentConfig as Config

    app.config.from_object(Config)

    app.register_blueprint(token.blueprint, url_prefix='/token')
    app.register_blueprint(profile.blueprint, url_prefix='/perfil')
    app.register_blueprint(report.blueprint, url_prefix='/relatorios')
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

    return app
