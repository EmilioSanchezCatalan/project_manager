"""
    Controladores destinados a las funcionalidades de los Centros
    sobre los TFMs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from project_manager.utils import render_to_pdf
from project_manager.settings import PAGINATION
from login.forms import CreateStudentForm
from login.models import Students
from login.decorators import is_center
from core.forms import CreateTutor2Form
from announcements.models import AnnouncementsTfm
from tfms.forms import FilterCenterTfmForm
from tfms.models import Tfms
from tfms.utils.update_tfm import UpdateTfm

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterTfmListView(ListView):

    """
        Controlador para mostrar el listado de tfms de una convocatoria.

        Atributos:
            model(model.Model): Modelo que se va a listar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
            paginate_by(int): Número de items por página.
    """

    model = Tfms
    template_name = "tfms/center_tfms_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset()

        # TFMs que corresponden con el id de la convocatoria,
        # cuya titulación corresponda al centro que la emite,
        # que hayan sido validados por departamento de forma positiva
        # y que no se encuentren en el borrador del profesor que lo ha creado.
        queryset = queryset.filter(
            announcements_id=self.kwargs['announ_id'],
            masters__centers=self.request.user.userinfos.centers,
            departament_validation=True,
            draft=False
        )

        # Opciones de filtrado de TFM (Titulo, Titulación, Departamento, Tutor, Estado)
        name = self.request.GET.get("search_text", "")
        master = self.request.GET.get("formation_project", "")
        departament = self.request.GET.get("departament", "")
        tutor = self.request.GET.get("tutor", "")
        status = self.request.GET.get("status", "")

        if name:
            queryset = queryset.filter(title__contains=name)
        if master:
            queryset = queryset.filter(masters_id=master)
        if departament:
            queryset = queryset.filter(tutor1__userinfos__departaments__id=departament)
        if tutor:
            queryset = queryset.filter(tutor1_id=tutor)
        if status:
            status = int(status)
            if status == Tfms.NOT_VALIDATED:
                queryset = queryset.filter(center_validation=None)
            elif status == Tfms.DEPARTAMENT_VALIDATION:
                queryset = queryset.filter(center_validation=True)
            elif status == Tfms.FAIL_VALIDATION:
                queryset = queryset.filter(
                    center_validation=False
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['form_filter'] = FilterCenterTfmForm(
            initial=self.request.GET.dict(),
            user=self.request.user
        )
        context['nbar'] = "tfm"
        context['announ'] = AnnouncementsTfm.objects.get(id=self.kwargs['announ_id'])

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

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterTfmDetailView(DetailView):

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
            masters__centers=self.request.user.userinfos.centers,
            departament_validation=True,
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfms_id=context['tfms'].id)
        context["back_url"] = "center_tfms_list"
        context["can_validate"] = True
        context["validation_url_ok"] = "center_tfms_validation_ok"
        context["validation_url_error"] = "center_tfms_validation_error"
        context["announ_id"] = self.kwargs["announ_id"]
        return context

    def get(self, request, *args, **kwargs):

        # En caso de querer renderizarlo en pdf
        if request.GET.get("format") == "pdf":
            pdf = render_to_pdf("tfms/tfms_format_pdf.html", { "tfm": self.get_object() })
            return HttpResponse(pdf, content_type="application/pdf")
        return super().get(request, *args, **kwargs)

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterTfmUpdateView(UpdateTfm):

    """
        Controlador de la vista editar de un TFM

        Atributos:
            template_name(str): template donde se va a renderizar la vista
    """

    template_name = "tfms/tfms_update_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Solo se puede editar si la convocatoria no está cerrada
        if self.object.announcements.status == AnnouncementsTfm.STATUS_CLOSE:
            messages.warning(
                self.request,
                "No es posible editar proyectos de una convocatoria cerrada",
                "warning"
            )
            announ_id = kwargs['announ_id']
            return HttpResponseRedirect(
                reverse('center_tfgs_list', kwargs={'announ_id': announ_id})
            )
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CenterTfmUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.get_object().tutor1
        return kwargs

    def get_success_url(self):
        announ_id = self.kwargs['announ_id']
        return reverse('center_tfms_list', kwargs={"announ_id": announ_id})

    def get_queryset(self):
        queryset = super(CenterTfmUpdateView, self).get_queryset()
        queryset = queryset.filter(
            masters__centers=self.request.user.userinfos.centers,
            departament_validation=True
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tfm = self.get_object()
        student = self._get_students_tfm(tfm)
        context["student_form"] = CreateStudentForm(prefix="student", instance=student[0])
        context["number_students"] = tfm.students.all().count()
        context["tutor2_form"] = CreateTutor2Form(prefix="tutor2", instance=tfm.tutor2)
        context["back_url"] = "center_tfms_list"
        context["edit"] = True
        context["announ_id"] = self.kwargs["announ_id"]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        student_form, tutor2_form = None, None
        form = self.get_form()
        form.instance = self.object
        if self.request.POST.get('has_student') == 'on':
            student_form = CreateStudentForm(
                self.request.POST,
                prefix="student",
                instance=self._get_student(
                    self.request.POST.get('student-dni')
                )
            )
            student_val = student_form.is_valid()
        else:
            student = self._get_student(self.request.POST.get('student-dni'))
            if student is not None:
                student.tfms = None
                student.save()
            student_val = True
        if self.request.POST.get('has_tutor2') == 'on':
            tutor2_form = CreateTutor2Form(
                self.request.POST,
                self.request.FILES,
                prefix="tutor2",
                instance=self.object.tutor2
            )
            tutor2_val = tutor2_form.is_valid()
        else:
            tutor2_val = True
        if form.is_valid() and student_val and tutor2_val:
            return self.form_valid(form, student_form, tutor2_form)
        else:
            return self.form_invalid(form, student_form, tutor2_form)

    def form_valid(self, form, student_form=None, tutor2_form=None):
        tutor2 = self._create_tutor2(tutor2_form)
        self._create_tfm(form, tutor2)
        self._create_student(self.object, student_form)
        messages.success(
            self.request,
            "Actualizado correctamente el trabajo fin de master con titulo: \""
            + self.object.title + "\"",
            'success'
        )
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, student_form=None, tutor2_form=None):
        if student_form is None:
            student_form = CreateStudentForm(prefix="student")
        if tutor2_form is None:
            tutor2_form = CreateTutor2Form(prefix="tutor2")
        self._errors_form(form)
        self._errors_form(student_form)
        self._errors_form(tutor2_form)
        return self.render_to_response(self.get_context_data(
            form=form,
            student1_form=student_form,
            tutor2_form=tutor2_form
        ))

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterValidationOk(RedirectView):

    """
        Controlador para manejar la validación positiva de un TFG

        Atributos:
            url(str): url donde se va a redireccionar.
            pattern_name(str): # TODO explicar
    """

    url = "center_tfms_list"
    pattern_name = 'validation'

    def get_redirect_url(self, *args, **kwargs):

        """
            Previamente a la redirección, modifica la validación del centro dejandola
            correcta (True) o eliminando la validación (None).

            Returns:
                url(str): Url donde se va a redirigir la vista.
        """
        try:
            tfm = Tfms.objects.get(
                id=kwargs['id'],
                masters__centers=self.request.user.userinfos.centers,
                departament_validation=True,
                announcements__status=AnnouncementsTfm.STATUS_OPEN
            )
            tfm.center_validation = True if kwargs['validate'] == 1 else None
            tfm.save()
            messages.success(self.request, "Validación realizada correctamente", "success")

        # TODO especificar una excepción concreta.
        # En caso de no encuentre el TFG.
        except Exception:
            messages.warning(
                self.request,
                "No se puede modificar la validación una vez que la "
                + "convocatoria deja de estar abierta a propuestas",
                "warning"
            )

        announ_id = kwargs['announ_id']
        url = reverse(
            super().get_redirect_url(*args, **kwargs),
            kwargs={"announ_id": announ_id}       
        )
        return url

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterValidationError(RedirectView):

    """
        Controlador para manejar la validación positiva de un TFG

        Atributos:
            url(str): url donde se va a redireccionar.
            pattern_name(str): # TODO explicar
    """

    url = "center_tfms_list"
    pattern_name = 'validation'

    def get_redirect_url(self, *args, **kwargs):

        """
            Previamente a la redirección, modifica la validación del centro dejandola
            negada (True) o eliminando la validación (None).

            Returns:
                url(str): Url donde se va a redirigir la vista.
        """
        try:
            tfm = Tfms.objects.get(
                id=kwargs['id'],
                masters__centers=self.request.user.userinfos.centers,
                departament_validation=True,
                announcements__status=AnnouncementsTfm.STATUS_OPEN
            )
            tfm.center_validation = False if kwargs['validate'] == 1 else None
            tfm.save()
            messages.success(self.request, "Validación realizada correctamente", "success")

        # TODO especificar una excepción concreta.
        # En caso de no encuentre el TFG.
        except Exception:
            messages.warning(
                self.request,
                "No se puede modificar la validación una vez que la "
                + "convocatoria deja de estar abierta a propuestas",
                "warning"
            )

        announ_id = kwargs['announ_id']
        url = reverse(
            super().get_redirect_url(*args, **kwargs),
            kwargs={"announ_id": announ_id}
        )
        return url
