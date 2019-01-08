"""
    Controladores destinados a las funcionalidades de los Profesores
    sobre los TFMs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from project_manager.utils import render_to_pdf
from project_manager.settings import PAGINATION
from login.forms import CreateStudentForm
from login.models import Students
from login.decorators import is_teacher
from core.forms import CreateTutor2Form
from announcements.models import AnnouncementsTfm
from tfms.forms import FilterTeacherTfmForm, CreateTfmForm
from tfms.models import Tfms
from tfms.utils.create_tfm import TfmCreateView
from tfms.utils.update_tfm import UpdateTfm

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfmListView(ListView):

    """
        Controlador para mostrar el listado de tfms destinados a la publicación.

        Atributos:
            model(model.Model): Modelo que se va a listar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
            paginate_by(int): Número de items por página.
    """

    model = Tfms
    template_name = "tfms/teacher_tfms_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user, draft=False)

        # Opciones de filtrado de TFM (Titulo, Titulación, Estado de la validación)
        name = self.request.GET.get("search_text", "")
        master = self.request.GET.get("formation_project", "")
        validation = self.request.GET.get("validation_state", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if master:
            queryset = queryset.filter(masters_id=master)
        if validation:
            validation = int(validation)
            if validation == Tfms.NOT_VALIDATED:
                queryset = queryset.filter(departament_validation=None, center_validation=None)
            elif validation == Tfms.DEPARTAMENT_VALIDATION:
                queryset = queryset.filter(departament_validation=True, center_validation=None)
            elif validation == Tfms.CENTER_VALIDATION:
                queryset = queryset.filter(departament_validation=True, center_validation=True)
            elif validation == Tfms.FAIL_VALIDATION:
                queryset = queryset.filter(
                    Q(departament_validation=False) | Q(center_validation=False)
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfms"
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['form_filter'] = FilterTeacherTfmForm(
            initial=self.request.GET.dict(),
            user=self.request.user
        )
        context['nbar'] = "tfm"
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

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfmDraftListView(ListView):

    """
        Controlador para mostrar el listado de tfms que se encuentran en el borrador.

        Atributos:
            model(model.Model): Modelo que se va a listar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
            paginate_by(int): Número de items por página.
    """

    model = Tfms
    template_name = "tfms/teacher_draft_tfms_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user, draft=True)

        # Opciones de filtrado de TFM (Titulo, Titulación)
        name = self.request.GET.get("search_text", "")
        carrer = self.request.GET.get("formation_project", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if carrer:
            queryset = queryset.filter(carrers_id=carrer)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['form_filter'] = FilterTeacherTfmForm(
            initial=self.request.GET.dict(),
            user=self.request.user
        )
        context['nbar'] = "tfm"
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

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfmDetailView(DetailView):

    """
        Controlador para mostrar un TFM en detalle.

        Atributos:
            model(model.Model): Modelo que se va a mostrar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
    """

    model = Tfms
    teamplate_name = "tfms/tfms_detail"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfms_id=context['tfms'].id)
        if self.object.draft:
            context["back_url"] = "teacher_draft_tfms_list"
        else:
            context["back_url"] = "teacher_tfms_list"
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get("format") == "pdf":
            pdf = render_to_pdf("tfms/tfms_format_pdf.html", {"tfm": self.get_object()})
            return HttpResponse(pdf, content_type="application/pdf")
        return super().get(request, *args, **kwargs)

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfmCreateView(TfmCreateView):

    """
        Controlador destinado a la creación de TFMs de publicación.

        Atributos
            success_url(str): url donde se redireccionará tras tener éxito al guardar.
            template_name(str): template en el que se va a renderizar la vista
    """

    success_url = reverse_lazy("teacher_tfms_list")
    template_name = "tfms/tfms_create_form.html"

    def _create_tfm(self, form, tutor2=None):
        self.object = form.save(commit=False)
        self.object.tutor1 = self.request.user
        self.object.tutor2 = tutor2
        announcement_open = self.object.carrers.centers.announcementstfm.filter(
            status=AnnouncementsTfm.STATUS_OPEN
        )
        if announcement_open:
            self.object.announcements = announcement_open[0]
            self.object.draft = False
        else:
            self.object.draft = True
            messages.warning(
                self.request,
                "No Existe convocatoria de publicación, con lo que se ha enviado "
                + "a Borradores",
                'warning'
            )
        self.object.save()
        form.save_m2m()

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherDraftTfmCreateView(TfmCreateView):

    """
        Controlador destinado a la creación de TFMs en borradores.

        Atributos
            success_url(str): url donde se redireccionará tras tener éxito al guardar.
            template_name(str): template en el que se va a renderizar la vista
    """

    success_url = reverse_lazy("teacher_tfms_list")
    template_name = "tfms/tfms_create_form.html"

    def _create_tfm(self, form, tutor2=None):
        self.object = form.save(commit=False)
        self.object.tutor1 = self.request.user
        self.object.tutor2 = tutor2
        self.object.draft = True
        self.object.save()
        form.save_m2m()


@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfmUpdateView(UpdateTfm):

    """
        Controlador de la vista editar de un tfm

        Atributos:
            template_name(str): template donde se va a renderizar la vista
    """

    model = Tfms
    form_class = CreateTfmForm
    template_name = "tfms/tfms_update_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.departament_validation is not None:
            messages.warning(self.request, "No es posible editar proyectos ya validados", "warning")
            return HttpResponseRedirect(reverse('teacher_tfms_list'))
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TeacherTfmUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        if self.object.draft == True:
            return reverse('teacher_draft_tfms_list')
        return reverse('teacher_tfms_list')

    def get_queryset(self):
        queryset = super(TeacherTfmUpdateView, self).get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tfm = self.get_object()
        student = self._get_students_tfm(tfm)
        context["student_form"] = CreateStudentForm(prefix="student", instance=student[0])
        context["number_students"] = tfm.students.all().count()
        context["tutor2_form"] = CreateTutor2Form(prefix="tutor2", instance=tfm.tutor2)
        context["edit"] = True
        if tfm.draft:
            context["back_url"] = "teacher_draft_tfms_list"
        else:
            context["back_url"] = "teacher_tfms_list"

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

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfmDelete(RedirectView):

    """
        Controlador para manejar la eliminación de un TFM

        Atributos:
            url(str): url donde se va a redireccionar.
            pattern_name(str): # TODO explicar
    """

    url = "teacher_tfms_list"
    pattern_name = 'delete_Tfm'

    def get_redirect_url(self, *args, **kwargs):

        """
            Previamente a la redirección, si es posible, se elimina el proyecto
            espeficicado.

            Returns:
                url(str): Url donde se va a redirigir la vista.
        """

        tfm = Tfms.objects.filter(id=kwargs['id'], tutor1=self.request.user).delete()

        # Comprobación de si es posible eliminar o no el TFM
        if tfm.departament_validation is None and tfm.departament_validation is None:
            tfm.delete()
            messages.success(self.request, "El proyecto se ha borrado correctamente", "success")
        else:
            messages.warning(self.request, "No se pueden eliminar proyectos validados", "warning")
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url
