"""
    Controladores destinados a las funcionalidades de los Centros
    sobre los tfms.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

import datetime
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from project_manager.utils import render_to_pdf
from project_manager.settings import PAGINATION
from login.models import Students
from announcements.models import AnnouncementsTfm
from tfms.forms import FilterPublicTfmForm, FilterPublicCenterForm, FilterPublicHistoryTfmForm
from tfms.models import Tfms
from core.models import Centers

class CentersListView(ListView):

    """
        Controlador encargado de mostrar el listado de centros

        Atributos:
            model(model.Model): Modelo que se va a listar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
            paginate_by(int): Número de items por página.
    """

    model = Centers
    template_name = "tfms/public_center_tfms_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset()

        # Opciones de filtrado de TFM (Titulo, Titulación)
        name = self.request.GET.get("center_name", "")
        if name:
            queryset = queryset.filter(name__contains=name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = FilterPublicCenterForm(initial=self.request.GET.dict())
        context['url_list_tfm'] = "public_tfms_list"
        return context

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
        context['announs'] = AnnouncementsTfm.objects.filter(
            status=AnnouncementsTfm.STATUS_PUBLIC,
            centers_id=self.kwargs['center_id']
        )
        center = Centers.objects.get(id=self.kwargs['center_id'])
        context['center'] = center
        context['form_filter'] = FilterPublicTfmForm(initial=self.request.GET.dict(), center=center)
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
        context["announ_id"] = self.kwargs['center_id']
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get("format") == "pdf":
            pdf = render_to_pdf("tfms/tfms_format_pdf.html", {"tfm": self.get_object()})
            return HttpResponse(pdf, content_type="application/pdf")
        return super().get(request, *args, **kwargs)

class CentersHistoryListView(ListView):

    """
        Controlador encargado de mostrar el listado de centros

        Atributos:
            model(model.Model): Modelo que se va a listar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
            paginate_by(int): Número de items por página.
    """

    model = Centers
    template_name = "tfms/public_center_tfms_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset()

        # Opciones de filtrado de TFM (Titulo, Titulación)
        name = self.request.GET.get("center_name", "")
        if name:
            queryset = queryset.filter(name__contains=name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = FilterPublicCenterForm(initial=self.request.GET.dict())
        context['url_list_tfm'] = "public_history_tfms_list"
        return context

class TfmHistoryListView(ListView):

    """
        Controlador encargado de mostrar el histórico público de los TFMs

        Atributos:
            model(model.Model): Modelo que se va a listar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
            paginate_by(int): Número de items por página.
    """

    model = Tfms
    template_name = "tfms/public_history_tfms_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(days=730)
        queryset = super().get_queryset().filter(
            masters__centers_id=self.kwargs['center_id'],
            departament_validation=True,
            center_validation=True,
            announcements__status=AnnouncementsTfm.STATUS_CLOSE,
            updatedAt__range=(earlier, now)
        )

        # Opciones de filtrado de TFM (Titulo, Titulación, Convocatoria)
        name = self.request.GET.get("name_project", "")
        master = self.request.GET.get("formation_project", "")
        announ = self.request.GET.get("announcements", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if master:
            queryset = queryset.filter(masters_id=master)
        if announ:
            queryset = queryset.filter(announcements__id=announ)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        center = Centers.objects.get(id=self.kwargs['center_id'])
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['center'] = center
        context['form_filter'] = FilterPublicHistoryTfmForm(
            initial=self.request.GET.dict(),
            center=center
        )
        return context

    @staticmethod
    def __check_filters_is_applied(params_dict):

        """
            Comprueba si hay aplicados filtros situados en la sección adicional de filtros.

            Parametros:
                params_dict(dict): diccionario con los query params de la url.

            Returns:
                Boolean: True o False en función si se cumple la condición mencionada.
        """

        for param_name in params_dict.keys():
            if param_name != "search_text" and params_dict[param_name] != "":
                return True
        return False

class TfmHistoryDetailView(DetailView):

    """
        Controlador para mostrar un TFM en detalle.

        Atributos:
            model(model.Model): Modelo que se va a mostrar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
    """

    model = Tfms
    teamplate_name = "tfms/tfms_detail"

    def get_queryset(self):
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(days=730)
        queryset = super().get_queryset().filter(
            departament_validation=True,
            center_validation=True,
            announcements__status=AnnouncementsTfm.STATUS_CLOSE,
            updatedAt__range=(earlier, now)
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfms_id=context['tfms'].id)
        context["back_url"] = "public_history_tfms_list"
        context["announ_id"] = self.kwargs['center_id']
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get("format") == "pdf":
            pdf = render_to_pdf("tfms/tfms_format_pdf.html", {"tfm": self.get_object()})
            return HttpResponse(pdf, content_type="application/pdf")
        return super().get(request, *args, **kwargs)
