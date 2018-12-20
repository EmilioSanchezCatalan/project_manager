"""
    Controladores destinados a las funcionalidades de los Centros
    sobre los tfms.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from project_manager.utils import render_to_pdf
from project_manager.settings import PAGINATION
from login.models import Students
from announcements.models import AnnouncementsTfm
from tfms.forms import FilterPublicTfmForm
from tfms.models import Tfms

class TfmListView(ListView):

    """
        Controlador encargado de mostrar el listado público de los TFMs

        Atributos:
            model(model.Model): Modelo que se va a listar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
            paginate_by(int): Número de items por página.
    """

    model = Tfms
    template_name = "tfms/public_tfms_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            departament_validation=True,
            center_validation=True,
            announcements__status=AnnouncementsTfm.STATUS_PUBLIC
        )

        # Opciones de filtrado de TFM (Titulo, Titulación)
        name = self.request.GET.get("name_project", "")
        master = self.request.GET.get("formation_project", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if master:
            queryset = queryset.filter(masters_id=master)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfms"
        context['form_filter'] = FilterPublicTfmForm(initial=self.request.GET.dict())
        return context

class TfmDetailView(DetailView):

    """
        Controlador para mostrar un TFM en detalle.

        Atributos:
            model(model.Model): Modelo que se va a mostrar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
    """

    model = Tfms
    teamplate_name = "tfms/tfms_detail"

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            departament_validation=True,
            center_validation=True
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfms_id=context['tfms'].id)
        context["back_url"] = "public_tfms_list"
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get("format") == "pdf":
            pdf = render_to_pdf("tfms/tfms_format_pdf.html", { "tfm": self.get_object() })
            return HttpResponse(pdf, content_type="application/pdf")
        return super().get(request, *args, **kwargs)
