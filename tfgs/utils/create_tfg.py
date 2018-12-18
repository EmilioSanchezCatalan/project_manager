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
from tfgs.forms import CreateTfgForm
from tfgs.models import Tfgs

class TfgCreateView(CreateView):

    """
        Controlador de la vista update generica para todos los usuarios.

        Atributos:
            model(Tfgs): Modelo TFG, el cual se va a editar.
            form_class(CreateTfgForm): formulario del Modelo TFG
    """

    model = Tfgs
    form_class = CreateTfgForm

    def get_form_kwargs(self):
        kwargs = super(TfgCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_form1"] = CreateStudentForm(prefix="student1")
        context["student_form2"] = CreateStudentForm(prefix="student2")
        context["tutor2_form"] = CreateTutor2Form(prefix="tutor2")
        context["back_url"] = "teacher_tfgs_list"
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        student1_form, student2_form, tutor2_form = None, None, None
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
            student1_val = True
        if self.request.POST.get('has_tutor2') == 'on':
            tutor2_form = CreateTutor2Form(
                self.request.POST,
                self.request.FILES,
                prefix="tutor2"
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
            student2_val = True
        if form.is_valid() and student1_val and tutor2_val and student2_val:
            return self.form_valid(form, student1_form, student2_form, tutor2_form)
        return self.form_invalid(form, student1_form, student2_form, tutor2_form)

    def form_valid(self, form, student1_form=None, student2_form=None, tutor2_form=None):
        tutor2 = self._create_tutor2(tutor2_form)
        self._create_tfg(form, tutor2)
        self._create_student(self.object, student1_form)
        self._create_student(self.object, student2_form)
        messages.success(
            self.request,
            "Creado correctamente nuevo trabajo fin de grado con titulo: \""
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

    def _create_tfg(self, form, tutor2=None):

        """
            Función encargada de crear un TFG dado su formulario y un tutor
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
    def _create_student(tfg, form=None):

        """
            Función que crear un nuevo estudiante en base de datos, asociandolo a un
            TFG.

            Parametros:
                tfg(Tfgs): modelo del TFG que se quiere asociar al estudiante.
                form(CreateStudentForm): formulario para la creación de un estudiante
        """

        if form is not None:
            student = form.save(commit=False)
            student.tfgs = tfg
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
