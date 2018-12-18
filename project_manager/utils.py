"""
    Funciones de utilidad para el proyecto.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(url_template, context={}):

    """
        Dado un template html y contexto renderiza un Modelo en un
        PDF

        Parametros:
            url_template(string): template HTML
            context(dict): información que enviar al template
    """
    template = get_template(url_template)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None
