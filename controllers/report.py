from flask import jsonify, request, send_file
from controllers.controller import Controller
from bs4 import BeautifulSoup as bs
from requests import Session
import io


class Report(Controller):

    def __init__(self):
        Controller.__init__(self, 'report', __name__)

    # @bp_report.route('/', methods=['GET'])
    def lista_relatorios(self):
        cookie = request.args.get('cookie')
        matricula = request.args.get('matricula')

        if not self.Autenticado(cookie):
            return jsonify({
                "code": 401,
                "error": "Nao autorizado"
            })

        self.sessao.cookies.set("JSESSIONID", cookie)
        siteRelatorios = self.sessao.get(self.URLS['relatorio_action_matricula'] + matricula)
        siteRelatoriosBS = bs(siteRelatorios.content, "html.parser")

        RelatoriosBrutos = siteRelatoriosBS.find_all('a', {'title': 'Relatório em formato PDF'})

        Relatorios = []
        for item in RelatoriosBrutos:
            relatorio = {}
            relatorio['id'] = RelatoriosBrutos.index(item)
            relatorio['nome'] = self.normalizacao(item.previousSibling)
            relatorio['link'] = item['href'].replace("/aluno/aluno/relatorio/", '')
            Relatorios.append(relatorio)

            return jsonify({
                "codigo": 200,
                "data": Relatorios
            })

    # @bp_report.route('/pdf', methods=['GET'])
    def geraRelatorio(self):
        cookie = request.args.get('cookie')
        link = request.args.get('link')

        if not self.Autenticado(cookie):
            return jsonify({
                "code": 401,
                "error": "Nao autorizado"
            })

        self.sessao.cookies.set("JSESSIONID", cookie)

        pdf_data = self.sessao.get(self.URLS['aluno_relatorio'] + link).content
        pdf = io.BytesIO()
        pdf.write(pdf_data)
        pdf.seek(0)

        return send_file(
            pdf,
            as_attachment=True,
            attachment_filename='relatorio.pdf',
            mimetype='application/pdf'
        )
