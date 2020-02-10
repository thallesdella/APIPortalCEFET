from controllers.controller import Controller
from bs4 import BeautifulSoup as bs


class Auth(Controller):

    def __init__(self):
        Controller.__init__(self, 'auth', __name__, False)

    def get_token(self, user, passwd):
        self.sessao.headers.update({'referer': self.URLS['matricula']})
        self.sessao.get(self.URLS['aluno_login_action_error'])

        dados_login = {"j_username": user, "j_password": passwd}

        sitePost = self.sessao.post(self.URLS['security_check'], data=dados_login)
        sitePostBS = bs(sitePost.content, "html.parser")

        Matricula = sitePostBS.find("input", id="matricula")["value"]
        Cookie = self.sessao.cookies.get_dict()

        if Cookie == '':
            self.error(403, 'Não Autorizado')

        return self.success_response(200, self._create_token(
            {
                "cookie": Cookie['JSESSIONID'],
                "matricula": Matricula
            }
        ))
