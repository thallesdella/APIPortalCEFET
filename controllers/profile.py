from flask import jsonify, request, send_file
from controllers.controller import Controller
from requests import Session
from bs4 import BeautifulSoup as bs
import io
import re


class Profile(Controller):

    def __init__(self):
        Controller.__init__(self, 'profile', __name__)

    def pegaPropriedadePerfil(self, conteudoHTML, propriedade):
        try:
            sitePerfilBS = bs(conteudoHTML, "html.parser")
            bloco = sitePerfilBS.find('span', text=re.compile(propriedade)).find_parent('td')

            objetoIgnorado = bloco.find('span')
            objetoIgnorado.extract()

            return self.normalizacao(bloco.get_text())

        except Exception as e:
            print('Exception:' + e)
            return None

    # @bp_profile.route('/', methods=['GET'])
    def perfilDados(self):  # @TODO: finalizar coleta de dados

        sessao = Session()

        cookie = request.args.get('cookie')
        matricula = request.args.get('matricula')

        if not self.Autenticado(cookie):
            return jsonify({
                "code": 401,
                "error": "Nao autorizado"
            })

        sessao.cookies.set("JSESSIONID", cookie)
        siteHorarios = sessao.get(Controller.URLS['menu_action_matricula'] + matricula)
        sitePerfil = sessao.get(Controller.URLS['perfil_perfil_action'])

        return jsonify(
            {
                "codigo": 200,
                "data": {
                    "Matricula": self.pegaPropriedadePerfil(siteHorarios.content, '.Matrícula:'),
                    "Curso": self.pegaPropriedadePerfil(siteHorarios.content, '.Curso:'),
                    "Periodo Atual": self.pegaPropriedadePerfil(siteHorarios.content, '.Período Atual:'),
                    "Nome": self.pegaPropriedadePerfil(sitePerfil.content, '.Nome')
                }
            }
        )

    # @bp_profile.route('/geral', methods=['GET'])
    def perfilDadosGerais(self):  # TODO: finalizar coleta de dados

        sessao = Session()

        cookie = request.args.get('cookie')
        matricula = request.args.get('matricula')
        sessao.cookies.set("JSESSIONID", cookie)

        if not self.Autenticado(cookie):
            return jsonify({
                "code": 401,
                "error": "Nao autorizado"
            })

        siteHorarios = sessao.get(Controller.URLS['menu_action_matricula'] + matricula)
        sitePerfil = sessao.get(Controller.URLS['perfil_perfil_action'])

        return jsonify({
            "codigo": 200,
            "data": {
                "academico": {
                    "Matricula": self.pegaPropriedadePerfil(siteHorarios.content, '.Matrícula:'),
                    "Curso": self.pegaPropriedadePerfil(siteHorarios.content, '.Curso:'),
                    "Periodo Atual": self.pegaPropriedadePerfil(siteHorarios.content, '.Período Atual:')
                },
                "informacoes": {
                    "Nome": self.pegaPropriedadePerfil(sitePerfil.content, '.Nome'),
                    "Nome da Mae": self.pegaPropriedadePerfil(sitePerfil.content, '.Nome da Mãe'),
                    "Nome do Pai": self.pegaPropriedadePerfil(sitePerfil.content, '.Nome da Pai'),
                    "Nascimento": self.pegaPropriedadePerfil(sitePerfil.content, '.Nascimento'),
                    "Sexo": self.pegaPropriedadePerfil(sitePerfil.content, '.Sexo'),
                    "Etnia": self.pegaPropriedadePerfil(sitePerfil.content, '.Etnia'),
                    "Deficiencia": self.pegaPropriedadePerfil(sitePerfil.content, '.Deficiência'),
                    "Tipo Sanguineo": self.pegaPropriedadePerfil(sitePerfil.content, '.Tipo Sanguíneo'),
                    "Fator RH": self.pegaPropriedadePerfil(sitePerfil.content, '.Fator RH'),
                    "Estado Civil": self.pegaPropriedadePerfil(sitePerfil.content, '.Estado Civil'),
                    "Pagina Pessoal": self.pegaPropriedadePerfil(sitePerfil.content, '.Página Pessoal'),
                    "Nacionalidade": self.pegaPropriedadePerfil(sitePerfil.content, '.Nacionalidade'),
                    "Estado": self.pegaPropriedadePerfil(sitePerfil.content, '.Estado'),
                    # TODO: consertar bug, Estado obtem Estado Civil
                    "Naturalidade": self.pegaPropriedadePerfil(sitePerfil.content, '.Naturalidade')
                },
                "endereco": {
                    "Tipo de endereco": self.pegaPropriedadePerfil(sitePerfil.content, '.Tipo de endereço'),
                    "Tipo de logradouro": self.pegaPropriedadePerfil(sitePerfil.content, '.Tipo de logradouro'),
                    "Logradouro": self.pegaPropriedadePerfil(sitePerfil.content, '.Logradouro'),
                    "Numero": self.pegaPropriedadePerfil(sitePerfil.content, '.Número'),
                    # TODO: consertar bug, Numero não é encontrado
                    "Complemento": self.pegaPropriedadePerfil(sitePerfil.content, '.Complemento'),
                    "Bairro": self.pegaPropriedadePerfil(sitePerfil.content, '.Bairro'),
                    "Pais": self.pegaPropriedadePerfil(sitePerfil.content, '.País'),
                    "Estado": self.pegaPropriedadePerfil(sitePerfil.content, '.Estado'),
                    # TODO: consertar bug, Estado obtem Estado Civil
                    "Cidade": self.pegaPropriedadePerfil(sitePerfil.content, '.Cidade'),
                    "Distrito": self.pegaPropriedadePerfil(sitePerfil.content, '.Distrito'),
                    "CEP": self.pegaPropriedadePerfil(sitePerfil.content, '.CEP'),
                    "Caixa Postal": self.pegaPropriedadePerfil(sitePerfil.content, '.Caixa Postal'),
                    "E-mail": self.pegaPropriedadePerfil(sitePerfil.content, '.E-mail'),
                    "Tel. Residencial": self.pegaPropriedadePerfil(sitePerfil.content, '.Tel. Residencial'),
                    "Tel. Celular": self.pegaPropriedadePerfil(sitePerfil.content, '.Tel. Celular'),
                    "Tel. Comercial": self.pegaPropriedadePerfil(sitePerfil.content, '.Tel. Comercial'),
                    "Fax": self.pegaPropriedadePerfil(sitePerfil.content, '.Fax')
                }
            }
        })

    # @bp_profile.route('/foto', methods=['GET'])
    def perfilFoto(self):
        sessao = Session()

        cookie = request.args.get('cookie')
        sessao.cookies.set("JSESSIONID", cookie)

        if not self.Autenticado(cookie):
            return jsonify({
                "code": 401,
                "error": "Nao autorizado"
            })

        img_data = sessao.get(Controller.URLS['foto_action']).content
        img = io.BytesIO()
        img.write(img_data)
        img.seek(0)

        return send_file(
            img,
            as_attachment=True,
            attachment_filename='imagemPerfil.jpeg',
            mimetype='image/jpeg'
        )
