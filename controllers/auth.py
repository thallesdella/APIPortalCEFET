from flask import jsonify, request
from controllers.controller import Controller
from bs4 import BeautifulSoup as bs


class Auth(Controller):

    def __init__(self):
        Controller.__init__(self, 'auth', __name__)

    def autenticacao(self):
        usuario = request.get_json().get('usuario')
        senha = request.get_json().get('senha')

        self.sessao.headers.update({'referer': self.URLS['matricula']})
        self.sessao.get(self.URLS['aluno_login_action_error'])

        dados_login = {"j_username": usuario, "j_password": senha}

        sitePost = self.sessao.post(self.URLS['security_check'], data=dados_login)
        sitePostBS = bs(sitePost.content, "html.parser")

        Matricula = sitePostBS.find("input", id="matricula")["value"]
        Cookie = self.sessao.cookies.get_dict()

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
