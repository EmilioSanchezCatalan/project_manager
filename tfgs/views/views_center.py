"""
    Controladores destinados a las funcionalidades de los Centros
    sobre los TFGs.

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
from announcements.models import AnnouncementsTfg
from tfgs.forms import FilterCenterTfgForm
from tfgs.models import Tfgs
from tfgs.utils.update_tfg import UpdateTfg

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterTfgListView(ListView):

    """
        Controlador para mostrar el listado de tfgs de una convocatoria.

        Atributos:
            model(model.Model): Modelo que se va a listar en la vista.
            template_name(str): Nombre del template donde se va a renderizar la vista.
            paginate_by(int): Número de items por página.
    """

    model = Tfgs
    template_name = "tfgs/center_tfgs_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):

        queryset = super().get_queryset()

        # TFGs que corresponden con el id de la convocatoria,
        # cuya titulación corresponda al centro que la emite,
        # que hayan sido validados por departamento de forma positiva
        # y que no se encuentren en el borrador del profesor que lo ha creado.
        queryset = queryset.filter(
            announcements_id=self.kwargs['announ_id'],
            carrers__centers=self.request.user.userinfos.centers,
            departament_validation=True,
            draft=False
        )

        # Opciones de filtrado de TFG (Titulo, Titulación, Departamento, Tutor)
        name = self.request.GET.get("search_text", "")
        carrer = self.request.GET.get("formation_project", "")
        departament = self.request.GET.get("departament", "")
        tutor = self.request.GET.get("tutor", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if carrer:
            queryset = queryset.filter(carrers_id=carrer)
        if departament:
            # TODO Revisar despues de borrar la ralción departamento
            queryset = queryset.filter(carrers__departament_id=departament)
        if tutor:
            queryset = queryset.filter(tutor1_id=tutor)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['form_filter'] = FilterCenterTfgForm(
            initial=self.request.GET.dict(),
            user=self.request.user
        )
        context['nbar'] = "tfg"
        context['announ'] = AnnouncementsTfg.objects.get(id=self.kwargs['announ_id'])
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
class CenterTfgDetailView(DetailView):

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
            carrers__centers=self.request.user.userinfos.centers,
            departament_validation=True
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfgs_id=context['tfgs'].id)
        context["back_url"] = "center_tfgs_list"
        context["can_validate"] = True
        context["validation_url_ok"] = "center_tfgs_validation_ok"
        context["validation_url_error"] = "center_tfgs_validation_error"
        context["announ_id"] = self.kwargs["announ_id"]
        return context

    def get(self, request, *args, **kwargs):

        # En caso de querer renderizarlo en pdf
        if request.GET.get("format") == "pdf":
            pdf = render_to_pdf("tfgs/tfgs_format_pdf.html", {"tfg": self.get_object()})
            return HttpResponse(pdf, content_type="application/pdf")
        return super().get(request, *args, **kwargs)

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterTfgUpdateView(UpdateTfg):

    """
        Controlador de la vista editar de un TFG

        Atributos:
            template_name(str): template donde se va a renderizar la vista
    """

    template_name = "tfgs/tfgs_update_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Solo se puede editar si la convocatoria no está cerrada
        if self.object.announcements.status == AnnouncementsTfg.STATUS_CLOSE:
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
        kwargs = super(CenterTfgUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.get_object().tutor1
        return kwargs

    def get_success_url(self):
        announ_id = self.kwargs['announ_id']
        return reverse('center_tfgs_list', kwargs={"announ_id": announ_id})

    def get_queryset(self):
        queryset = super(CenterTfgUpdateView, self).get_queryset()
        queryset = queryset.filter(
            carrers__centers=self.request.user.userinfos.centers,
            departament_validation=True,
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tfg = self.get_object()
        list_students = self._get_students_tfg(tfg)
        context["student_form1"] = CreateStudentForm(prefix="student1", instance=list_students[0])
        context["student_form2"] = CreateStudentForm(prefix="student2", instance=list_students[1])
        context["number_students"] = tfg.students.all().count()
        context["tutor2_form"] = CreateTutor2Form(prefix="tutor2", instance=tfg.tutor2)
        context["back_url"] = "center_tfgs_list"
        context["edit"] = True
        context["announ_id"] = self.kwargs["announ_id"]
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
            "Actualizado correctamente el trabajo fin de grado "
            + "con titulo: \"" + self.object.title + "\"",
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

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterValidationOk(RedirectView):

    """
        Controlador para manejar la validación positiva de un TFG

        Atributos:
            url(str): url donde se va a redireccionar.
            pattern_name(str): # TODO explicar
    """

    url = "center_tfgs_list"
    pattern_name = 'validation'

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
                carrers__centers=self.request.user.userinfos.centers,
                departament_validation=True,
                announcements__status=AnnouncementsTfg.STATUS_OPEN
            )
            tfg.center_validation = True if kwargs['validate'] == 1 else None
            tfg.save()
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
        Controlador para manejar la validación negativa de un TFG

        Atributos:
            url(str): url donde se va a redireccionar.
            pattern_name(str): # TODO explicar
    """

    url = "center_tfgs_list"
    pattern_name = 'validation'

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
                carrers__centers=self.request.user.userinfos.centers,
                departament_validation=True,
                announcements__status=AnnouncementsTfg.STATUS_OPEN
            )
            tfg.center_validation = False if kwargs['validate'] == 1 else None
            tfg.save()
            messages.success(self.request, "Validación realizada correctamente", "success")

        # TODO especificar una excepción concreta.
        # En caso de no encuentre el TFG.
        except Exception:
            messages.warning(
                self.request,
                "No se puede modificar la validación una vez que la convocatoria"
                + " deja de estar abierta a propuestas",
                "warning"
            )

        announ_id = kwargs['announ_id']
        url = reverse(
            super().get_redirect_url(*args, **kwargs), 
            kwargs={"announ_id": announ_id}
        )
        return url
