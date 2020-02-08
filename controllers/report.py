from flask import jsonify, request, send_file, Blueprint
from bs4 import BeautifulSoup as bs
from requests import Session
import controllers.helpers as helpers
import io

bp_report = Blueprint('report', __name__)


@bp_report.route('/', methods=['GET'])
def lista_relatorios():
    sessao = Session()

    cookie = request.args.get('cookie')
    matricula = request.args.get('matricula')

    if not helpers.Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    sessao.cookies.set("JSESSIONID", cookie)
    siteRelatorios = sessao.get(helpers.URLS['relatorio_action_matricula'] + matricula)
    siteRelatoriosBS = bs(siteRelatorios.content, "html.parser")

    RelatoriosBrutos = siteRelatoriosBS.find_all('a', {'title': 'Relatório em formato PDF'})

    Relatorios = []
    for item in RelatoriosBrutos:
        relatorio = {}
        relatorio['id'] = RelatoriosBrutos.index(item)
        relatorio['nome'] = helpers.normalizacao(item.previousSibling)
        relatorio['link'] = item['href'].replace("/aluno/aluno/relatorio/", '')
        Relatorios.append(relatorio)

        return jsonify({
            "codigo": 200,
            "data": Relatorios
        })


@bp_report.route('/pdf', methods=['GET'])
def geraRelatorio():
    sessao = Session()

    cookie = request.args.get('cookie')
    link = request.args.get('link')

    if not helpers.Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    sessao.cookies.set("JSESSIONID", cookie)

    pdf_data = sessao.get(helpers.URLS['aluno_relatorio'] + link).content
    pdf = io.BytesIO()
    pdf.write(pdf_data)
    pdf.seek(0)

    return send_file(
        pdf,
        as_attachment=True,
        attachment_filename='relatorio.pdf',
        mimetype='application/pdf'
    )
