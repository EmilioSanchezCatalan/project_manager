"""
    Controladores destinados a las funcionalidades de los Centros
    sobre los TFGs.

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
from announcements.models import AnnouncementsTfg
from tfgs.forms import FilterPublicTfgForm
from tfgs.models import Tfgs

class TfgListView(ListView):

    """
        Controlador encargado de mostrar el listado público de los TFGs

        Atributos:
            model(model.Model): Modelo que se va a listar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
            paginate_by(int): Número de items por página.
    """

    model = Tfgs
    template_name = "tfgs/public_tfgs_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            departament_validation=True,
            center_validation=True,
            announcements__status=AnnouncementsTfg.STATUS_PUBLIC
        )

        # Opciones de filtrado de TFG (Titulo, Titulación)
        name = self.request.GET.get("name_project", "")
        carrer = self.request.GET.get("formation_project", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if carrer:
            queryset = queryset.filter(carrers_id=carrer)
        return queryset

    def get_context_data(self, **kwargs):

        """
            Comprueba si hay aplicados filtros situados en la sección adicional de filtros.

            Parametros:
                params_dict(dict): diccionario con los query params de la url.

            Returns:
                Boolean: True o False en función si se cumple la condición mencionada.
        """

        context = super().get_context_data(**kwargs)
        context['form_filter'] = FilterPublicTfgForm(initial=self.request.GET.dict())
        return context

class TfgDetailView(DetailView):

    """
        Controlador para mostrar un TFG en detalle.

        Atributos:
            model(model.Model): Modelo que se va a mostrar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
    """

    model = Tfgs
    teamplate_name = "tfgs/tfgs_detail"

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            departament_validation=True,
            center_validation=True
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfgs_id=context['tfgs'].id)
        context["back_url"] = "public_tfgs_list"
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get("format") == "pdf":
            pdf = render_to_pdf("tfgs/tfgs_format_pdf.html", { "tfg": self.get_object() })
            return HttpResponse(pdf, content_type="application/pdf")
        return super().get(request, *args, **kwargs)
