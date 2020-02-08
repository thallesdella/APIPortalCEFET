from flask import Blueprint, make_response, jsonify, request, abort
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

    blueprint = None

    cookie = None

    matricula = None

    def __init__(self, name, import_name):
        self.blueprint = Blueprint(name, import_name)
        self.sessao = Session()

    def normalizacao(self, texto):
        return unicodedata.normalize('NFKD', texto) \
            .encode('ASCII', 'ignore').decode('ASCII') \
            .replace('  ', '').replace('\n', '') \
            .replace('\r', '')

    def Autenticado(self):
        if not request.headers['X-Token']:
            return False

        self.cookie = request.headers['X-Token']
        self.sessao.cookies.set("JSESSIONID", self.cookie)
        self.sessao.headers.update({'referer': self.URLS['matricula']})

        acesso = self.sessao.get(self.URLS['index_action'], allow_redirects=False)

        if acesso.status_code == 302:
            return False
        else:
            return True

    @staticmethod
    def error(code, message):
        abort(code, description=message)
        # return make_response(jsonify({"code": code, "error": message}), code)

    @staticmethod
    def success_response(code, data):
        return make_response(jsonify({"code": code, "data": data}), code)
