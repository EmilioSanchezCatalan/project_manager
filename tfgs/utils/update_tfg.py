"""
    Clase customizada para la vista update de un TFG.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.views.generic.edit import UpdateView
from django.contrib import messages
from login.models import Students
from tfgs.models import Tfgs
from tfgs.forms import CreateTfgForm
from announcements.models import AnnouncementsTfg

class UpdateTfg(UpdateView):

    """
        Controlador de la vista update generica para todos los usuarios.

        Atributos:
            model(Tfgs): Modelo TFG, el cual se va a editar.
            form_class(CreateTfgForm): formulario del Modelo TFG

    """

    model = Tfgs
    form_class = CreateTfgForm

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

        self.object = form.save(commit=False)
        self.object.tutor2 = tutor2
        if self.request.user.groups.filter(name="Teachers").exists():
            if not self.object.draft:
                announcement_open = self.object.carrers.centers.announcementstfg.filter(
                    status=AnnouncementsTfg.STATUS_OPEN
                )
                if announcement_open:
                    self.object.announcements = announcement_open[0]
                    self.object.draft = False
                else:
                    self.object.draft = True
                    messages.warning(
                        self.request,
                        "No Existe convocatoria de publicación, "
                        + "con lo que se ha enviado a Borradores",
                        'warning'
                    )
            else:
                self.object.announcements = None
        else:
            self.object.draft = False
        self.object.save()
        form.save_m2m()

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
        # TODO establecer excepción correcta
        except Exception:
            return None

    @staticmethod
    def _get_students_tfg(tfg):

        """
            Función que obtiene y devuelve el listado de alumnos asociados a un
            TFG.

            Parametros:
                tfg(Tfgs): modelo del TFG en el que se quiere buscar sus estudiantes

            Returns:
                Students(2): devuelve un array de 2 elementos con los estudiantes
                    que estan asociados al tfg. (el maximo son 2).
        """

        list_students = [None, None]
        students = tfg.students.all()
        number_students = students.count()
        if number_students > 0:
            list_students[0] = students[0]
        if number_students > 1:
            list_students[1] = students[1]
        return list_students

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
