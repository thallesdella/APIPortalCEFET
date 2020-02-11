from flask import Blueprint, make_response, jsonify, request, abort
from source.core.jwt import Jwt
from requests import Session
import unicodedata


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

    def __init__(self, name, import_name, validate_token=True):
        self.blueprint = Blueprint(name, import_name)
        self.sessao = Session()
        self.__token = None
        self._jwt = Jwt()

        if validate_token:
            self.__validate_client()

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token):
        self.__token = token
        self._jwt._token = token
        return

    def __validate_client(self):
        if (not request.headers['X-Token']) or (not self._jwt.validate_token()):
            self.error(400, 'Insira um token valido')

        self.token = request.headers['X-Token']

        token_data = self._jwt.get_token_data()
        self.sessao.cookies.set("JSESSIONID", token_data['cookie'])

        if not self.__auth_client():
            self.error(403, 'Não Autorizado')
        return

    def __auth_client(self):
        self.sessao.headers.update({'referer': self.URLS['matricula']})

        acesso = self.sessao.get(self.URLS['index_action'], allow_redirects=False)
        if acesso.status_code == 302:
            return False
        else:
            return True

    @staticmethod
    def normalizacao(text):
        return unicodedata.normalize('NFKD', text) \
            .encode('ASCII', 'ignore').decode('ASCII') \
            .replace('  ', '').replace('\n', '') \
            .replace('\r', '')

    @staticmethod
    def error(code, message):
        abort(code, description=message)
        return

    @staticmethod
    def success_response(code, data):
        return make_response(jsonify({"code": code, "data": data}), code)