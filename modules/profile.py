from flask import jsonify, request, send_file
from requests import Session
from bs4 import BeautifulSoup as bs
import modules.helpers as helpers
import io
import re


def pegaPropriedadePerfil(conteudoHTML, propriedade):
    try:
        sitePerfilBS = bs(conteudoHTML, "html.parser")
        bloco = sitePerfilBS.find('span', text=re.compile(propriedade)).find_parent('td')

        objetoIgnorado = bloco.find('span')
        objetoIgnorado.extract()

        return helpers.normalizacao(bloco.get_text())

    except Exception as e:
        print('Exception:' + e)
        return None


@app.route('/perfil', methods=['GET'])
def perfilDados():  # @TODO: finalizar coleta de dados

    sessao = Session()

    cookie = request.args.get('cookie')
    matricula = request.args.get('matricula')

    if not helpers.Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    sessao.cookies.set("JSESSIONID", cookie)
    siteHorarios = sessao.get(helpers.URLS['menu_action_matricula'] + matricula)
    sitePerfil = sessao.get(helpers.URLS['perfil_perfil_action'])

    return jsonify(
        {
            "codigo": 200,
            "data": {
                "Matricula": pegaPropriedadePerfil(siteHorarios.content, '.Matrícula:'),
                "Curso": pegaPropriedadePerfil(siteHorarios.content, '.Curso:'),
                "Periodo Atual": pegaPropriedadePerfil(siteHorarios.content, '.Período Atual:'),
                "Nome": pegaPropriedadePerfil(sitePerfil.content, '.Nome')
            }
        }
    )


@app.route('/perfil/geral', methods=['GET'])
def perfilDadosGerais():  # TODO: finalizar coleta de dados

    sessao = Session()

    cookie = request.args.get('cookie')
    matricula = request.args.get('matricula')
    sessao.cookies.set("JSESSIONID", cookie)

    if not helpers.Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    siteHorarios = sessao.get(helpers.URLS['menu_action_matricula'] + matricula)
    sitePerfil = sessao.get(helpers.URLS['perfil_perfil_action'])

    return jsonify({
        "codigo": 200,
        "data": {
            "academico": {
                "Matricula": pegaPropriedadePerfil(siteHorarios.content, '.Matrícula:'),
                "Curso": pegaPropriedadePerfil(siteHorarios.content, '.Curso:'),
                "Periodo Atual": pegaPropriedadePerfil(siteHorarios.content, '.Período Atual:')
            },
            "informacoes": {
                "Nome": pegaPropriedadePerfil(sitePerfil.content, '.Nome'),
                "Nome da Mae": pegaPropriedadePerfil(sitePerfil.content, '.Nome da Mãe'),
                "Nome do Pai": pegaPropriedadePerfil(sitePerfil.content, '.Nome da Pai'),
                "Nascimento": pegaPropriedadePerfil(sitePerfil.content, '.Nascimento'),
                "Sexo": pegaPropriedadePerfil(sitePerfil.content, '.Sexo'),
                "Etnia": pegaPropriedadePerfil(sitePerfil.content, '.Etnia'),
                "Deficiencia": pegaPropriedadePerfil(sitePerfil.content, '.Deficiência'),
                "Tipo Sanguineo": pegaPropriedadePerfil(sitePerfil.content, '.Tipo Sanguíneo'),
                "Fator RH": pegaPropriedadePerfil(sitePerfil.content, '.Fator RH'),
                "Estado Civil": pegaPropriedadePerfil(sitePerfil.content, '.Estado Civil'),
                "Pagina Pessoal": pegaPropriedadePerfil(sitePerfil.content, '.Página Pessoal'),
                "Nacionalidade": pegaPropriedadePerfil(sitePerfil.content, '.Nacionalidade'),
                "Estado": pegaPropriedadePerfil(sitePerfil.content, '.Estado'),
                # TODO: consertar bug, Estado obtem Estado Civil
                "Naturalidade": pegaPropriedadePerfil(sitePerfil.content, '.Naturalidade')
            },
            "endereco": {
                "Tipo de endereco": pegaPropriedadePerfil(sitePerfil.content, '.Tipo de endereço'),
                "Tipo de logradouro": pegaPropriedadePerfil(sitePerfil.content, '.Tipo de logradouro'),
                "Logradouro": pegaPropriedadePerfil(sitePerfil.content, '.Logradouro'),
                "Numero": pegaPropriedadePerfil(sitePerfil.content, '.Número'),
                # TODO: consertar bug, Numero não é encontrado
                "Complemento": pegaPropriedadePerfil(sitePerfil.content, '.Complemento'),
                "Bairro": pegaPropriedadePerfil(sitePerfil.content, '.Bairro'),
                "Pais": pegaPropriedadePerfil(sitePerfil.content, '.País'),
                "Estado": pegaPropriedadePerfil(sitePerfil.content, '.Estado'),
                # TODO: consertar bug, Estado obtem Estado Civil
                "Cidade": pegaPropriedadePerfil(sitePerfil.content, '.Cidade'),
                "Distrito": pegaPropriedadePerfil(sitePerfil.content, '.Distrito'),
                "CEP": pegaPropriedadePerfil(sitePerfil.content, '.CEP'),
                "Caixa Postal": pegaPropriedadePerfil(sitePerfil.content, '.Caixa Postal'),
                "E-mail": pegaPropriedadePerfil(sitePerfil.content, '.E-mail'),
                "Tel. Residencial": pegaPropriedadePerfil(sitePerfil.content, '.Tel. Residencial'),
                "Tel. Celular": pegaPropriedadePerfil(sitePerfil.content, '.Tel. Celular'),
                "Tel. Comercial": pegaPropriedadePerfil(sitePerfil.content, '.Tel. Comercial'),
                "Fax": pegaPropriedadePerfil(sitePerfil.content, '.Fax')
            }
        }
    })


@app.route('/perfil/foto', methods=['GET'])
def perfilFoto():
    sessao = Session()

    cookie = request.args.get('cookie')
    sessao.cookies.set("JSESSIONID", cookie)

    if not helpers.Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    img_data = sessao.get(helpers.URLS['foto_action']).content
    img = io.BytesIO()
    img.write(img_data)
    img.seek(0)

    return send_file(
        img,
        as_attachment=True,
        attachment_filename='imagemPerfil.jpeg',
        mimetype='image/jpeg'
    )
