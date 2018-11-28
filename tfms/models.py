from django.db import models
from core.models import Tutor2, Masters

# Create your models here.
class Tfms(models.Model):

    # Tipo de tfm
    TYPE_UNI = 0
    TYPE_BUSINESS = 1
    TYPE_CHOICE = (
        (TYPE_BUSINESS, 'Empresa'),
        (TYPE_UNI, 'Universidad'),
    )

    # Campos del modelo
    title = models.CharField(max_length=255, verbose_name="Título")
    type = models.PositiveSmallIntegerField(verbose_name="Tipo de proyecto", choices=TYPE_CHOICE)
    objectives = models.TextField(verbose_name="objectivos")
    methodology = models.TextField(verbose_name="Metodología")
    docs_and_forms = models.TextField(verbose_name="Documentos y formatos de entrega")
    language = models.CharField(max_length=45, verbose_name="Idioma")
    knowledge = models.TextField(null=True, verbose_name="Conocimientos requeridos", blank=True)
    departament_validation = models.BooleanField(null=True, verbose_name="Validación del departamento")
    center_validation = models.BooleanField(null=True, verbose_name="Validación del centro")
    tutor1 = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Tutor principal")
    tutor2 = models.ForeignKey(Tutor2, on_delete=models.CASCADE, null=True, verbose_name="Tutor de apoyo", blank=True)
    masters = models.ForeignKey(Masters, on_delete=models.CASCADE, verbose_name="Master")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.title)

    class Meta:
        ordering = ['-createdAt']
        verbose_name = 'Trabajo final de master'
        verbose_name_plural = 'Trabajos finales de master'

