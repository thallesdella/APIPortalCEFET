from flask import Blueprint, make_response, jsonify, request, abort
from jwcrypto import jwt, jwk
from requests import Session
import unicodedata
import json


class Controller:
    URLS = {
        'matricula': 'https://alunos.cefet-rj.br/matricula/',
        'index_action': 'https://alunos.cefet-rj.br/aluno/index.action',
        'foto_action': 'https://alunos.cefet-rj.br/aluno/aluno/foto.action',
        'menu_action_matricula': 'https://alunos.cefet-rj.br/aluno/aluno/quadrohorario/menu.action?matricula=',
        'perfil_perfil_action': 'https://alunos.cefet-rj.br/aluno/aluno/perfil/perfil.action',
        'aluno_relatorio': 'https://alunos.cefet-rj.br/aluno/aluno/relatorio/',
        'relatorio_action_matricula': 'https://alunos.cefet-rj.br/aluno/aluno/relatorio/relatorios.action?matricula=',
        'aluno_login_action_error': 'https://alunos.cefet-rj.br/aluno/login.action?error=',
        'security_check': 'https://alunos.cefet-rj.br/aluno/j_security_check'
    }

    blueprint = None

    def __init__(self, name, import_name, validate_token=True):
        self.blueprint = Blueprint(name, import_name)
        self.sessao = Session()
        self.__token = request.headers['X-Token']

        if validate_token:
            if not self.auth_token():
                self.error(403, 'Não Autorizado')
            else:
                self.sessao.cookies.set("JSESSIONID", self.__token)

    def auth_token(self):
        if not request.headers['X-Token']:
            return False

        self.sessao.cookies.set("JSESSIONID", self.__token)
        self.sessao.headers.update({'referer': self.URLS['matricula']})

        acesso = self.sessao.get(self.URLS['index_action'], allow_redirects=False)

        if acesso.status_code == 302:
            return False
        else:
            return True

    def __validate_token(self):

        key = jwk.JWK(**json.loads(self.__key))
        dec_jwt = jwt.JWT().deserialize(jwt=self.__token, key=key)
        return dec_jwt.token.is_valid

    @staticmethod
    def normalizacao(text):
        return unicodedata.normalize('NFKD', text) \
            .encode('ASCII', 'ignore').decode('ASCII') \
            .replace('  ', '').replace('\n', '') \
            .replace('\r', '')

    @staticmethod
    def error(code, message):
        abort(code, description=message)

    @staticmethod
    def success_response(code, data):
        return make_response(jsonify({"code": code, "data": data}), code)
