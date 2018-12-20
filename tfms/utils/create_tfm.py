"""
    Clase customizada para la vista create de un TFG.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from login.forms import CreateStudentForm
from login.models import Students
from core.forms import CreateTutor2Form
from tfms.forms import CreateTfmForm
from tfms.models import Tfms

class TfmCreateView(CreateView):

    """
        Controlador de la vista update generica para todos los usuarios.

        Atributos:
            model(Tfgs): Modelo TFG, el cual se va a editar.
            form_class(CreateTfgForm): formulario del Modelo TFG
    """

    model = Tfms
    form_class = CreateTfmForm

    def get_form_kwargs(self):
        kwargs = super(TfmCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_form"] = CreateStudentForm(prefix="student")
        context["tutor2_form"] = CreateTutor2Form(prefix="tutor2")
        context["back_url"] = "teacher_tfms_list"
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        student_form, tutor2_form = None, None
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
            student_val = True
        if self.request.POST.get('has_tutor2') == 'on':
            tutor2_form = CreateTutor2Form(
                self.request.POST,
                self.request.FILES,
                prefix="tutor2"
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
            "Creado correctamente nuevo trabajo final de master con titulo: \""
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
            student_form=student_form,
            tutor2_form=tutor2_form
        ))

    def _errors_form(self, form):

        """
            Función encargada de checkear los errores de un formulario.

            Parametros:
                form(form.Modelform): formulario del que se va a checkear, si existen errores.
        """

        form_errors = form.errors
        for fields_error in form_errors.keys():
            for error in form_errors[fields_error]:
                messages.error(self.request, fields_error + ": " + error, 'danger')

    def _create_tfm(self, form, tutor2=None):

        """
            Función encargada de crear un TFM dado su formulario y un tutor
            de forma opcional.

            Parametros:
                form(CreateTfgForm): formulario de creación de TFG
                tutor2(Tutor2): modelo tutor secundario asociado al TFG (opcional)
        """

        pass

    @staticmethod
    def _get_student(dni):

        """
            Función que obtiene un estudiante apartir de un numero identificador(dni).

            Parametros:
                dni(str): dni que debe de ser único para cada alumno.

            Returns:
                Students: devuelve el modelo con el alumno que tiene dicho dni.
                None: en caso de no encontrarlo.
        """

        try:
            return Students.objects.get(dni=dni)

        # TODO Exception especific
        except:
            return None

    @staticmethod
    def _create_student(tfm, form=None):

        """
            Función que crear un nuevo estudiante en base de datos, asociandolo a un
            TFM.

            Parametros:
                tfm(Tfms): modelo del TFM que se quiere asociar al estudiante.
                form(CreateStudentForm): formulario para la creación de un estudiante
        """

        if form is not None:
            student = form.save(commit=False)
            student.tfms = tfm
            student.save()

    @staticmethod
    def _create_tutor2(form=None):

        """
            Función encargada de crear un nuevo tutor secundario en base de datos.

            Parametros:
                form(Tutor2): formulario para la creación de un nuevo tutor secundario

            Returns:
                Tutor2: devuelve el modelo guardado con el nuevo tutor secundario
        """

        if form is not None:
            return form.save()
        return None
