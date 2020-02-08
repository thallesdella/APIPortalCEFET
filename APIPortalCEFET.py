from flask import Flask, jsonify

from controllers.profile import bp_profile
from controllers.report import bp_report
from controllers.schedule import bp_schedule

import os

app = Flask(__name__)
app.register_blueprint(bp_profile, url_prefix='/perfil')
app.register_blueprint(bp_report, url_prefix='/relatorios')
app.register_blueprint(bp_schedule, url_prefix='/horarios')


@app.errorhandler(404)
def respond404(error):
    return jsonify({
        "code": 404,
        "error": "Nao encontrado"
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)  # para prod, ative aqui!
    #app.run(debug=True, host='127.0.0.1', port=port)  # para dev, ative aqui!
