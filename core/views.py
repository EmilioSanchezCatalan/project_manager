"""
    Controladores de la vistas principales

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.views.generic.base import TemplateView

class HomePageView(TemplateView):

    """
        Controlador de la vista principal.
    """

    template_name = "core/home.html"
