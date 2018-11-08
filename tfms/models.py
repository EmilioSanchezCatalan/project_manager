from django.db import models
from core.models import Tutor2, Masters

# Create your models here.
class Tfms(models.Model):

    # Tipo de tfm
    TYPE_UNI = 0
    TYPE_BUSINESS = 1

    # Modo de tfm
    MODE_INVESTIGATOR = 0
    MODE_PROFESSIONALIZING = 1

    # Campos del modelo
    title = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField()
    mode = models.PositiveSmallIntegerField()
    objectives = models.TextField()
    methodology = models.TextField()
    docs_and_forms = models.TextField()
    language = models.CharField(max_length=45)
    knowledge = models.TextField()
    departament_validation = models.BooleanField()
    center_validation = models.BooleanField()
    tutor1 = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tutor2 = models.ForeignKey(Tutor2, on_delete=models.CASCADE, null=True)
    masters = models.ForeignKey(Masters, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
