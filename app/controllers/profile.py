from flask import send_file
from app.controllers.controller import Controller
from bs4 import BeautifulSoup as bs
import io
import re


class Profile(Controller):

    def __init__(self):
        Controller.__init__(self, 'profile', __name__)

    def perfilDados(self):  # @TODO: finalizar coleta de dados
        siteHorarios = self.sessao.get(Controller.URLS['menu_action_matricula'] + self.matricula)
        sitePerfil = self.sessao.get(Controller.URLS['perfil_perfil_action'])

        return self.success_response(200, {
            "Matricula": self._pegaPropriedadePerfil(siteHorarios.content, '.Matrícula:'),
            "Curso": self._pegaPropriedadePerfil(siteHorarios.content, '.Curso:'),
            "Periodo Atual": self._pegaPropriedadePerfil(siteHorarios.content, '.Período Atual:'),
            "Nome": self._pegaPropriedadePerfil(sitePerfil.content, '.Nome')
        })

    def perfilDadosGerais(self):  # TODO: finalizar coleta de dados
        siteHorarios = self.sessao.get(Controller.URLS['menu_action_matricula'] + self.matricula)
        sitePerfil = self.sessao.get(Controller.URLS['perfil_perfil_action'])

        return self.success_response(200, {
            "academico": {
                "Matricula": self._pegaPropriedadePerfil(siteHorarios.content, '.Matrícula:'),
                "Curso": self._pegaPropriedadePerfil(siteHorarios.content, '.Curso:'),
                "Periodo Atual": self._pegaPropriedadePerfil(siteHorarios.content, '.Período Atual:')
            },
            "informacoes": {
                "Nome": self._pegaPropriedadePerfil(sitePerfil.content, '.Nome'),
                "Nome da Mae": self._pegaPropriedadePerfil(sitePerfil.content, '.Nome da Mãe'),
                "Nome do Pai": self._pegaPropriedadePerfil(sitePerfil.content, '.Nome da Pai'),
                "Nascimento": self._pegaPropriedadePerfil(sitePerfil.content, '.Nascimento'),
                "Sexo": self._pegaPropriedadePerfil(sitePerfil.content, '.Sexo'),
                "Etnia": self._pegaPropriedadePerfil(sitePerfil.content, '.Etnia'),
                "Deficiencia": self._pegaPropriedadePerfil(sitePerfil.content, '.Deficiência'),
                "Tipo Sanguineo": self._pegaPropriedadePerfil(sitePerfil.content, '.Tipo Sanguíneo'),
                "Fator RH": self._pegaPropriedadePerfil(sitePerfil.content, '.Fator RH'),
                "Estado Civil": self._pegaPropriedadePerfil(sitePerfil.content, '.Estado Civil'),
                "Pagina Pessoal": self._pegaPropriedadePerfil(sitePerfil.content, '.Página Pessoal'),
                "Nacionalidade": self._pegaPropriedadePerfil(sitePerfil.content, '.Nacionalidade'),
                "Estado": self._pegaPropriedadePerfil(sitePerfil.content, '.Estado'),
                # TODO: consertar bug, Estado obtem Estado Civil
                "Naturalidade": self._pegaPropriedadePerfil(sitePerfil.content, '.Naturalidade')
            },
            "endereco": {
                "Tipo de endereco": self._pegaPropriedadePerfil(sitePerfil.content, '.Tipo de endereço'),
                "Tipo de logradouro": self._pegaPropriedadePerfil(sitePerfil.content, '.Tipo de logradouro'),
                "Logradouro": self._pegaPropriedadePerfil(sitePerfil.content, '.Logradouro'),
                "Numero": self._pegaPropriedadePerfil(sitePerfil.content, '.Número'),
                # TODO: consertar bug, Numero não é encontrado
                "Complemento": self._pegaPropriedadePerfil(sitePerfil.content, '.Complemento'),
                "Bairro": self._pegaPropriedadePerfil(sitePerfil.content, '.Bairro'),
                "Pais": self._pegaPropriedadePerfil(sitePerfil.content, '.País'),
                "Estado": self._pegaPropriedadePerfil(sitePerfil.content, '.Estado'),
                # TODO: consertar bug, Estado obtem Estado Civil
                "Cidade": self._pegaPropriedadePerfil(sitePerfil.content, '.Cidade'),
                "Distrito": self._pegaPropriedadePerfil(sitePerfil.content, '.Distrito'),
                "CEP": self._pegaPropriedadePerfil(sitePerfil.content, '.CEP'),
                "Caixa Postal": self._pegaPropriedadePerfil(sitePerfil.content, '.Caixa Postal'),
                "E-mail": self._pegaPropriedadePerfil(sitePerfil.content, '.E-mail'),
                "Tel. Residencial": self._pegaPropriedadePerfil(sitePerfil.content, '.Tel. Residencial'),
                "Tel. Celular": self._pegaPropriedadePerfil(sitePerfil.content, '.Tel. Celular'),
                "Tel. Comercial": self._pegaPropriedadePerfil(sitePerfil.content, '.Tel. Comercial'),
                "Fax": self._pegaPropriedadePerfil(sitePerfil.content, '.Fax')
            }
        })

    def perfilFoto(self):
        img_data = self.sessao.get(Controller.URLS['foto_action']).content
        img = io.BytesIO()
        img.write(img_data)
        img.seek(0)

        return send_file(
            img,
            as_attachment=True,
            attachment_filename='imagemPerfil.jpeg',
            mimetype='image/jpeg'
        )

    def _pegaPropriedadePerfil(self, conteudoHTML, propriedade):
        try:
            sitePerfilBS = bs(conteudoHTML, "html.parser")
            bloco = sitePerfilBS.find('span', text=re.compile(propriedade)).find_parent('td')

            objetoIgnorado = bloco.find('span')
            objetoIgnorado.extract()

            return self.normalizacao(bloco.get_text())

        except Exception as e:
            print('Exception:' + e)
            return None
