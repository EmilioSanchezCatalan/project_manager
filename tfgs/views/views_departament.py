"""
    Controladores destinados a las funcionalidades de los Departamentos
    sobre los TFGs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.http import HttpResponseRedirect, HttpResponse
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
from login.decorators import is_departaments
from core.forms import CreateTutor2Form
from tfgs.forms import  FilterDepartamentTfgForm
from tfgs.models import Tfgs
from tfgs.utils.update_tfg import UpdateTfg

@method_decorator(user_passes_test(is_departaments), name="dispatch")
class DepartamentTfgListView(ListView):

    """
        Controlador para mostrar el listado de tfgs.

        Atributos:
            model(model.Model): Modelo que se va a listar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
            paginate_by(int): Número de items por página.
    """

    model = Tfgs
    template_name = "tfgs/departament_tfgs_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            tutor1__userinfos__departaments=self.request.user.userinfos.departaments,
        )
        queryset = queryset.exclude(announcements=None)

        # Opciones de filtrado de TFG (Titulo, Titulación, Area, Tutor, Estado)
        name = self.request.GET.get("search_text", "")
        carrer = self.request.GET.get("formation_project", "")
        area = self.request.GET.get("area", "")
        tutor = self.request.GET.get("tutor", "")
        status = self.request.GET.get("status", "")

        if name:
            queryset = queryset.filter(title__icontains=name)
        if carrer:
            queryset = queryset.filter(carrers_id=carrer)
        if area:
            queryset = queryset.filter(tutor1__userinfos__areas_id=area)
        if tutor:
            queryset = queryset.filter(tutor1_id=tutor)
        if status:
            status = int(status)
            if status == Tfgs.NOT_VALIDATED:
                queryset = queryset.filter(departament_validation=None)
            elif status == Tfgs.DEPARTAMENT_VALIDATION:
                queryset = queryset.filter(departament_validation=True)
            elif status == Tfgs.FAIL_VALIDATION:
                queryset = queryset.filter(
                    departament_validation=False
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['form_filter'] = FilterDepartamentTfgForm(
            initial=self.request.GET.dict(),
            user=self.request.user
        )
        context['nbar'] = "tfg"
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

@method_decorator(user_passes_test(is_departaments), name="dispatch")
class DepartamentTfgDetailView(DetailView):

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
            tutor1__userinfos__departaments=self.request.user.userinfos.departaments,
            draft=False
        )
        queryset = queryset.exclude(announcements=None)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfgs_id=context['tfgs'].id)
        context["back_url"] = "departament_tfgs_list"
        context["can_validate"] = True
        context["validation_url_ok"] = "departament_tfgs_validation_ok"
        context["validation_url_error"] = "departament_tfgs_validation_error"
        return context

    def get(self, request, *args, **kwargs):

        # En caso de querer renderizarlo en pdf
        if request.GET.get("format") == "pdf":
            pdf = render_to_pdf("tfgs/tfgs_format_pdf.html", {"tfg": self.get_object()})
            return HttpResponse(pdf, content_type="application/pdf")
        return super().get(request, *args, **kwargs)

@method_decorator(user_passes_test(is_departaments), name="dispatch")
class DepartamentTfgUpdateView(UpdateTfg):

    """
        Controlador de la vista editar de un TFG

        Atributos:
            template_name(str): template donde se va a renderizar la vista
    """

    template_name = "tfgs/tfgs_update_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.departament_validation is not None:
            messages.warning(
                self.request,
                "No es posible editar proyectos ya validados",
                "warning"
            )
            return HttpResponseRedirect(reverse('departament_tfgs_list'))
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(DepartamentTfgUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.get_object().tutor1
        return kwargs

    def get_success_url(self):
        return reverse('departament_tfgs_list')

    def get_queryset(self):
        queryset = super(DepartamentTfgUpdateView, self).get_queryset()
        queryset = queryset.filter(
            tutor1__userinfos__departaments=self.request.user.userinfos.departaments,
            draft=False
        )
        queryset = queryset.exclude(announcements=None)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tfg = self.get_object()
        list_students = self._get_students_tfg(tfg)
        context["student_form1"] = CreateStudentForm(prefix="student1", instance=list_students[0])
        context["student_form2"] = CreateStudentForm(prefix="student2", instance=list_students[1])
        context["number_students"] = tfg.students.all().count()
        context["tutor2_form"] = CreateTutor2Form(prefix="tutor2", instance=tfg.tutor2)
        context["back_url"] = "departament_tfgs_list"
        context["edit"] = True
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        student1_form, student2_form, tutor2_form = None, None, None
        form = self.get_form()
        form.instance = self.object
        if self.request.POST.get('has_student') == 'on':
            student1_form = CreateStudentForm(
                self.request.POST,
                prefix="student1",
                instance=self._get_student(
                    self.request.POST.get('student1-dni')
                )
            )
            student1_val = student1_form.is_valid()
        else:
            student = self._get_student(self.request.POST.get('student1-dni'))
            if student is not None:
                student.tfgs = None
                student.save()
            student1_val = True
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
        if (self.request.POST.get('has_student') == 'on' and
                self.request.POST.get('is_team') == 'on'):
            student2_form = CreateStudentForm(
                self.request.POST,
                prefix="student2",
                instance=self._get_student(
                    self.request.POST.get('student2-dni')
                )
            )
            student2_val = student2_form.is_valid()
        else:
            student = self._get_student(self.request.POST.get('student2-dni'))
            if student is not None:
                student.tfgs = None
                student.save()
            student2_val = True
        if form.is_valid() and student1_val and tutor2_val and student2_val:
            return self.form_valid(form, student1_form, student2_form, tutor2_form)
        else:
            return self.form_invalid(form, student1_form, student2_form, tutor2_form)

    def form_valid(self, form, student1_form=None, student2_form=None, tutor2_form=None):
        tutor2 = self._create_tutor2(tutor2_form)
        self._create_tfg(form, tutor2)
        self._create_student(self.object, student1_form)
        self._create_student(self.object, student2_form)
        messages.success(
            self.request,
            "Actualizado correctamente el trabajo fin de grado con titulo: \""
            + self.object.title + "\"",
            'success'
        )
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, student1_form=None, student2_form=None, tutor2_form=None):
        if student1_form is None:
            student1_form = CreateStudentForm(prefix="student1")
        if student2_form is None:
            student2_form = CreateStudentForm(prefix="student2")
        if tutor2_form is None:
            tutor2_form = CreateTutor2Form(prefix="tutor2")

        self._errors_form(form)
        self._errors_form(student1_form)
        self._errors_form(student2_form)
        self._errors_form(tutor2_form)
        return self.render_to_response(self.get_context_data(
            form=form,
            student1_form=student1_form,
            student2_form=student2_form,
            tutor2_form=tutor2_form
        ))

@method_decorator(user_passes_test(is_departaments), name="dispatch")
class DepartamentValidationOk(RedirectView):

    """
        Controlador para manejar la validación positiva de un TFG

        Atributos:
            url(str): url donde se va a redireccionar.
            pattern_name(str): # TODO explicar
    """

    url = "departament_tfgs_list"
    pattern_name = 'validation_ok'

    def get_redirect_url(self, *args, **kwargs):

        """
            Previamente a la redirección, modifica la validación del centro dejandola
            correcta (True) o eliminando la validación (None).

            Returns:
                url(str): Url donde se va a redirigir la vista.
        """

        # En caso de que exista el TFG con las propiedades seleccionadas
        try:
            tfg = Tfgs.objects.get(
                id=kwargs['id'],
                tutor1__userinfos__departaments=self.request.user.userinfos.departaments,
                center_validation=None
            )
            tfg.departament_validation = True if kwargs['validate'] == 1 else None
            tfg.save()
            messages.success(self.request, "Validación realizada correctamente", "success")

        # TODO especificar una excepción concreta.
        # En caso de no encuentre el TFG.
        except Exception:
            messages.warning(
                self.request,
                "No se puede modificar la validación una vez que el"
                + " centro ha validado",
                "warning"
            )
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url

@method_decorator(user_passes_test(is_departaments), name="dispatch")
class DepartamentValidationError(RedirectView):

    """
        Controlador para manejar la validación negativa de un TFG

        Atributos:
            url(str): url donde se va a redireccionar.
            pattern_name(str): # TODO explicar
    """

    url = "departament_tfgs_list"
    pattern_name = 'validation_error'

    def get_redirect_url(self, *args, **kwargs):

        """
            Previamente a la redirección, modifica la validación del centro dejandola
            negativa (False) o eliminando la validación (None).

            Returns:
                url(str): Url donde se va a redirigir la vista.
        """

        # En caso de que exista el TFG con las propiedades seleccionadas
        try:
            tfg = Tfgs.objects.get(
                id=kwargs['id'],
                tutor1__userinfos__departaments=self.request.user.userinfos.departaments,
                center_validation=None
            )
            tfg.departament_validation = False if kwargs['validate'] == 1 else None
            tfg.save()
            messages.success(self.request, "Validación realizada correctamente", "success")

        # TODO especificar una excepción concreta.
        # En caso de no encuentre el TFG.
        except Exception:
            messages.warning(
                self.request,
                "No se puede modificar la validación una vez que el centro ha"
                + " validado",
                "warning"
            )

        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url
