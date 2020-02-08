from flask import Flask, jsonify, request
from bs4 import BeautifulSoup as bs
from requests import Session

from modules.profile import bp_profile
from modules.report import bp_report
from modules.schedule import bp_schedule
import modules.helpers as helpers

import os

app = Flask(__name__)
app.register_blueprint(bp_profile, url_prefix='perfil')
app.register_blueprint(bp_report, url_prefix='relatorios')
app.register_blueprint(bp_schedule, url_prefix='horarios')


@app.route('/autenticacao', methods=['POST'])
def autenticacao():
    sessao = Session()

    usuario = request.get_json().get('usuario')
    senha = request.get_json().get('senha')

    sessao.headers.update({'referer': helpers.URLS['matricula']})
    sessao.get(helpers.URLS['aluno_login_action_error'])

    dados_login = {"j_username": usuario, "j_password": senha}

    sitePost = sessao.post(helpers.URLS['security_check'], data=dados_login)
    sitePostBS = bs(sitePost.content, "html.parser")

    Matricula = sitePostBS.find("input", id="matricula")["value"]
    Cookie = sessao.cookies.get_dict()

    if Cookie == '':
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    return jsonify({
        "code": 200,
        "data": {
            "matricula": Matricula,
            "cookie": Cookie['JSESSIONID']
        }
    })

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
