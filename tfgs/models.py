from django.db import models
from core.models import Carrers
from core.models import Mentions, Tutor2, Itineraries, Skills

# Create your models here.
class Tfgs(models.Model):

    # Tipo de tfg
    TYPE_GENERAL = 0
    TYPE_ESPECIFIC = 1
    TYPE_CHOICE = (
        (TYPE_GENERAL, 'General'),
        (TYPE_ESPECIFIC, 'Específico')
    )

    # Modo del tfg
    MODE_ING_PROYECT = 0
    MODE_TECHNICAL_STUDY = 1
    MODE_EXP_THEORETICAL = 2
    MODE_CHOICE = (
        (MODE_EXP_THEORETICAL, 'Trabajo teórico/experimental'),
        (MODE_ING_PROYECT, 'Proyecto de Ingeniería'),
        (MODE_TECHNICAL_STUDY, 'Estudio técnico')
    )

    # Campos del modelo
    title = models.CharField(max_length=255, verbose_name="Título")
    type = models.PositiveSmallIntegerField(verbose_name="Tipo de proyecto", choices=TYPE_CHOICE)
    mode = models.PositiveSmallIntegerField(verbose_name="Modalidad", choices=MODE_CHOICE)
    is_team = models.BooleanField(verbose_name="¿Es un trabajo en equipo?")
    objectives = models.TextField(verbose_name="Objetivos")
    methodology = models.TextField(verbose_name="Metodología")
    docs_and_forms = models.TextField(verbose_name="Documentos y formatos de entrega")
    departament_validation = models.BooleanField(null=True, verbose_name="Validación del departamento")
    center_validation = models.BooleanField(null=True, verbose_name="Validación del centro")
    tutor1 = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="tutor1", verbose_name="Tutor principal")
    tutor2 = models.ForeignKey(Tutor2, on_delete=models.CASCADE, null=True, verbose_name="Tutor de apoyo", blank=True)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE, related_name="tfgs", verbose_name="Titulación")
    itineraries = models.ForeignKey(Itineraries, on_delete=models.CASCADE, null=True, verbose_name="Itinerario", blank=True)
    mentions = models.ForeignKey(Mentions, on_delete=models.CASCADE, null=True, verbose_name="Mencion", blank=True)
    skills = models.ManyToManyField(Skills, verbose_name="Competencias que desarrolla")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.title)

    class Meta:
        ordering = ['-createdAt']
        verbose_name = 'Trabajo final de grado'
        verbose_name_plural = 'Trabajos finales de grado'
