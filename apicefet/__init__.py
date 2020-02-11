from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

db = SQLAlchemy()


def create_app(env='develop'):
    app = Flask(__name__, instance_relative_config=False)

    if env == 'production':
        from configs.production_config import ProductionConfig as Config
    else:
        from configs.development_config import DevelopmentConfig as Config

    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from apicefet.controllers.token.routes import token
        from apicefet.controllers.profile.routes import profile
        from apicefet.controllers.reports.routes import report
        from apicefet.controllers.schedule.routes import schedule
        from apicefet.controllers.errors import handle_http_exception

        app.register_blueprint(token.blueprint, url_prefix='/token')
        app.register_blueprint(profile.blueprint, url_prefix='/perfil')
        app.register_blueprint(report.blueprint, url_prefix='/relatorios')
        app.register_blueprint(schedule.blueprint, url_prefix='/horarios')

        db.create_all()

        app.register_error_handler(HTTPException, handle_http_exception)

    return app
