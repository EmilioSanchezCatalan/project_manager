"""
    Controladores destinados a las funcionalidades para controlar
    las convocatorias de TFGs

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

import datetime
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from project_manager.settings import PAGINATION
from login.decorators import is_center
from tfms.models import Tfms
from announcements.models import AnnouncementsTfm
from announcements.forms import FilterAnnouncementsForm, CreateAnnouncementsTfmForm

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfmListView(ListView):

    """
        Controlador para listar las convocatorias de los TFMs.

        Atributos
            model(models.Model): Modelo que se quiere listar.
            template_name(str): template donde se va a renderizar la vista.
            paginate_by(int): numero de items por página.

    """

    model = AnnouncementsTfm
    template_name = "announcements/announcements_tfm_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset().filter(centers=self.request.user.userinfos.centers)
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__contains=name)
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = FilterAnnouncementsForm(initial=self.request.GET.dict())
        context['nbar'] = "tfm"
        return context

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfmCreateView(CreateView):

    """
        Controlador para la actualización de la información de una
        convocatoria.

        Atributos
            model(models.Model): Modelo que se quiere crear.
            template_name(str): template donde se va a renderizar la vista.
            form_class(forms.Modelform): formulario para la creación del modelo.
            success_url(str): url de redirección cuando todo a ido correctamente.

    """

    model = AnnouncementsTfm
    template_name = "announcements/announcements_form.html"
    form_class = CreateAnnouncementsTfmForm
    success_url = reverse_lazy("announ_tfms_list")

    def get(self, request, *args, **kwargs):
        announ = AnnouncementsTfm.objects.filter(centers_id=self.request.user.userinfos.centers.id)
        announ = announ.exclude(status=AnnouncementsTfm.STATUS_CLOSE)
        if AnnouncementsTfm.objects.exclude(status=AnnouncementsTfm.STATUS_CLOSE):
            messages.warning(self.request, "Ya tiene una convocatoria abierta en curso", 'warning')
            return HttpResponseRedirect(reverse("announ_tfms_list"))
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = "announ_tfms_list"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = AnnouncementsTfm.STATUS_OPEN
        self.object.centers = self.request.user.userinfos.centers
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfmUpdateView(UpdateView):

    """
        Controlador para la actualización de la información de una
        convocatoria.

        Atributos
            model(models.Model): Modelo que se quiere editar.
            template_name(str): template donde se va a renderizar la vista.
            form_class(forms.Modelform): formulario para la edición del modelo.
            success_url(str): url de redirección cuando todo a ido correctamente.
    """

    model = AnnouncementsTfm
    template_name = "announcements/announcements_form.html"
    form_class = CreateAnnouncementsTfmForm
    success_url = reverse_lazy("announ_tfms_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = "announ_tfms_list"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.centers = self.request.user.userinfos.centers
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfmPublicStatus(RedirectView):

    """
        Controlador para cambiar el estado a público de los TFMs

        Atributos:
            url(str): dirección de redirección.
            pattern_name(str): TODO explicar
    """

    url = "announ_tfms_list"
    pattern_name = 'public_announ_tfm'

    def get_redirect_url(self, *args, **kwargs):

        """
            Función que cambia el estado a público de una convocatoria antes de realizar
            la redirección (solo si el estado actual es abierto).
        """

        announ = AnnouncementsTfm.objects.get(
            id=kwargs['id'],
            centers=self.request.user.userinfos.centers
        )
        if announ.status == AnnouncementsTfm.STATUS_OPEN:
            announ.status = AnnouncementsTfm.STATUS_PUBLIC
            announ.save()
            messages.success(
                self.request, "Se ha modificado el estado a \'"
                + AnnouncementsTfm.STATUS_TEXT_PUBLIC + "\'",
                'success'
            )
        else:
            messages.error(
                self.request,
                "La convocatoria no se encuentra en el estado: \'"
                + AnnouncementsTfm.STATUS_TEXT_OPEN + "\'",
                'danger'
            )
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfmCloseStatus(RedirectView):

    """
        Controlador para cambiar el estado a cerrado de los TFMs

        Atributos:
            url(str): dirección de redirección.
            pattern_name(str): TODO explicar
    """

    url = "announ_tfms_list"
    pattern_name = 'public_announ_tfm'

    def get_redirect_url(self, *args, **kwargs):

        """
            Función que cambia el estado a cerrado una convocatoria antes de realizar
            la redirección (solo si el estado actual es público).
        """

        announ = AnnouncementsTfm.objects.get(
            id=kwargs['id'],
            centers=self.request.user.userinfos.centers
        )
        if announ.status == AnnouncementsTfm.STATUS_PUBLIC:
            announ.status = AnnouncementsTfm.STATUS_CLOSE
            announ.save()
            self.not_assigned_tfms(announ.id)
            messages.error(
                self.request,
                "Se ha modificado el estado a \'" + AnnouncementsTfm.STATUS_TEXT_CLOSE + "\'",
                'success'
            )
        else:
            messages.error(
                self.request,
                "La convocatoria no se encuentra en el estado: \'"
                + AnnouncementsTfm.STATUS_TEXT_PUBLIC + "\'",
                'danger'
            )
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url

    @staticmethod
    def not_assigned_tfms(announ_id):

        """
            Función encargada de desasignar TFMs a convocatorias y establecer el estado
            borrador a true, de aquellos TFMs que no tiene asignación de estudiantes

            Parametros:
                announ_id(int): identificador de la convocatoria.
        """

        queryset = Tfms.objects.filter(announcements=announ_id)
        for query in queryset:
            if len(query.students.all()) <= 0:
                query.draft = True
                query.announcements = None
                query.save()
            else:
                query.date_assignment = datetime.datetime.now()
                query.save()

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfmDeleteView(RedirectView):

    """
        Controlador para la eliminación de convocatorias de TFMs.

        Atributos:
            url(str): dirección de redirección.
            pattern_name(str): TODO explicar

    """
    url = "announ_tfms_list"
    pattern_name = 'delete_Tfm'

    def get_redirect_url(self, *args, **kwargs):

        """
            Función que elimina una convocatoria antes de realizar la redirección
            (solo se pueden borrar convocatorias en estado cerrado).
        """

        announ = AnnouncementsTfm.objects.get(
            id=kwargs['id'],
            centers=self.request.user.userinfos.centers
        )
        if announ.status != AnnouncementsTfm.STATUS_CLOSE:
            announ.delete()
            messages.success(self.request, "La convocatoria se ha borrado correctamente", "success")
        else:
            messages.warning(self.request, "No se puede borrar una convocatoria cerrada", "warning")
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url
