"""
    Clase customizada para la vista update de un TFG.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.views.generic.edit import UpdateView
from django.contrib import messages
from login.models import Students
from tfms.models import Tfms
from tfms.forms import CreateTfmForm
from announcements.models import AnnouncementsTfm

class UpdateTfm(UpdateView):

    """
        Controlador de la vista update generica para todos los usuarios.

        Atributos:
            model(Tfms): Modelo TFG, el cual se va a editar.
            form_class(CreateTfgForm): formulario del Modelo TFM

    """

    model = Tfms
    form_class = CreateTfmForm

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
            Función encargada de crear un TFG dado su formulario y un tutor
            de forma opcional.

            Parametros:
                form(CreateTfgForm): formulario de creación de TFM
                tutor2(Tutor2): modelo tutor secundario asociado al TFM (opcional)
        """

        self.object = form.save(commit=False)
        self.object.tutor2 = tutor2
        if self.request.user.groups.filter(name="Teachers").exists():
            if not self.object.draft:
                announcement_open = self.object.masters.centers.announcementstfm.filter(
                    status=AnnouncementsTfm.STATUS_OPEN
                )
                print(announcement_open)
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
        except:
            return None

    @staticmethod
    def _get_students_tfm(tfm):

        """
            Función que obtiene y devuelve el listado de alumnos asociados a un
            TFM.

            Parametros:
                tfm(Tfms): modelo del TFM en el que se quiere buscar sus estudiantes

            Returns:
                Students(2): devuelve un array de 2 elementos con los estudiantes
                    que estan asociados al tfm. (el maximo son 2).
        """

        students = [None]
        students_list = tfm.students.all()
        if students_list.count() > 0:
            students = students_list
        return students

    @staticmethod
    def _create_student(tfm, form=None):

        """
            Función que crear un nuevo estudiante en base de datos, asociandolo a un
            TFM.

            Parametros:
                tfm(Tfms): modelo del TFG que se quiere asociar al estudiante.
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
