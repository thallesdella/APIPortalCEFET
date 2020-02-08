from flask import send_file
from controllers.controller import Controller
from bs4 import BeautifulSoup as bs
import io


class Report(Controller):

    def __init__(self):
        Controller.__init__(self, 'report', __name__)

    def lista_relatorios(self):
        if not self.Autenticado():
            return self.error_response(403, 'Não Autorizado')

        self.sessao.cookies.set("JSESSIONID", self.cookie)
        siteRelatorios = self.sessao.get(self.URLS['relatorio_action_matricula'] + self.matricula)
        siteRelatoriosBS = bs(siteRelatorios.content, "html.parser")

        RelatoriosBrutos = siteRelatoriosBS.find_all('a', {'title': 'Relatório em formato PDF'})

        Relatorios = []
        for item in RelatoriosBrutos:
            relatorio = {}
            relatorio['id'] = RelatoriosBrutos.index(item)
            relatorio['nome'] = self.normalizacao(item.previousSibling)
            relatorio['link'] = item['href'].replace("/aluno/aluno/relatorio/", '')
            Relatorios.append(relatorio)

            return self.success_response(200, Relatorios)

    def geraRelatorio(self, url):
        if not self.Autenticado():
            return self.error_response(403, 'Não Autorizado')

        self.sessao.cookies.set("JSESSIONID", self.cookie)

        pdf_data = self.sessao.get(self.URLS['aluno_relatorio'] + url).content
        pdf = io.BytesIO()
        pdf.write(pdf_data)
        pdf.seek(0)

        return send_file(
            pdf,
            as_attachment=True,
            attachment_filename='relatorio.pdf',
            mimetype='application/pdf'
        )
