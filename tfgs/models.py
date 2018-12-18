"""
    Modelos de la app TFGs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from django.db import models
from ckeditor.fields import RichTextField
from core.models import Carrers
from core.models import Mentions, Tutor2, Itineraries, Skills
from announcements.models import AnnouncementsTfg

# Create your models here.
class Tfgs(models.Model):

    """
        Modelo en el que se alvergarán la información referente a los
        TFGs
    """

    # Tipo de tfg
    TYPE_GENERAL = 0
    TYPE_TEXT_GENERAL = "General"
    TYPE_ESPECIFIC = 1
    TYPE_TEXT_ESPECIFIC = "Específico"
    TYPE_CHOICE = (
        (TYPE_GENERAL, TYPE_TEXT_GENERAL),
        (TYPE_ESPECIFIC, TYPE_TEXT_ESPECIFIC)
    )

    # Modo del tfg
    MODE_ING_PROYECT = 0
    MODE_TEXT_ING_PROYECT = "Proyecto de Ingeniería"
    MODE_TECHNICAL_STUDY = 1
    MODE_TEXT_TECHNICAL_STUDY = "Estudio técnico"
    MODE_EXP_THEORETICAL = 2
    MODE_TEXT_EXP_THEORETICAL = "Trabajo teórico/experimental"
    MODE_CHOICE = (
        (MODE_ING_PROYECT, MODE_TEXT_ING_PROYECT),
        (MODE_TECHNICAL_STUDY, MODE_TEXT_TECHNICAL_STUDY),
        (MODE_EXP_THEORETICAL, MODE_TEXT_EXP_THEORETICAL)
    )

    # Estado de Validacion
    NOT_VALIDATED = 0
    DEPARTAMENT_VALIDATION = 1
    CENTER_VALIDATION = 2
    FAIL_VALIDATION = 3

    # Campos del modelo
    title = models.CharField(max_length=255, verbose_name="Título")
    type = models.PositiveSmallIntegerField(verbose_name="Tipo de proyecto", choices=TYPE_CHOICE)
    mode = models.PositiveSmallIntegerField(verbose_name="Modalidad", choices=MODE_CHOICE)
    is_team = models.BooleanField(verbose_name="¿Es un trabajo en equipo?")
    team_memory = models.FileField(
        verbose_name="Memoria justificativa",
        upload_to="is_team",
        blank=True,
        null=True
    )
    objectives = RichTextField(verbose_name="Objetivos")
    methodology = RichTextField(verbose_name="Metodología")
    docs_and_forms = RichTextField(verbose_name="Documentos y formatos de entrega")
    departament_validation = models.BooleanField(
        null=True,
        verbose_name="Validación del departamento"
    )
    center_validation = models.BooleanField(null=True, verbose_name="Validación del centro")
    draft = models.BooleanField(verbose_name="Borrador")
    date_assignment = models.DateTimeField(verbose_name="Fecha de asignación", null=True)
    tutor1 = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name="tutor1",
        verbose_name="Tutor principal"
    )
    tutor2 = models.ForeignKey(
        Tutor2,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Tutor de apoyo",
        blank=True
    )
    carrers = models.ForeignKey(
        Carrers,
        on_delete=models.CASCADE,
        related_name="tfgs",
        verbose_name="Titulación"
    )
    itineraries = models.ForeignKey(
        Itineraries,
        on_delete=models.CASCADE, verbose_name="Itinerario")
    mentions = models.ForeignKey(
        Mentions,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Mencion",
        blank=True
    )
    announcements = models.ForeignKey(
        AnnouncementsTfg,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Convocatoria"
    )
    skills = models.ManyToManyField(Skills, verbose_name="Competencias que desarrolla")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.title)

    class Meta:
        ordering = ['-createdAt']
        verbose_name = 'Trabajo final de grado'
        verbose_name_plural = 'Trabajos finales de grado'
