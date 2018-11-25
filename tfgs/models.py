from django.db import models
from core.models import Carrers
from core.models import Mentions, Tutor2, Itineraries, Skills

# Create your models here.
class Tfgs(models.Model):

    # Tipo de tfg
    TYPE_GENERAL = 0
    TYPE_ESPECIFIC = 1

    # Modo del tfg
    MODE_ING_PROYECT = 0
    MODE_TECHNICAL_STUDY = 1
    MODE_EXP_THEORETICAL = 2

    # Campos del modelo
    title = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField()
    mode = models.PositiveSmallIntegerField()
    is_team = models.BooleanField()
    objectives = models.TextField()
    methodology = models.TextField()
    docs_and_forms = models.TextField()
    departament_validation = models.BooleanField(null=True)
    center_validation = models.BooleanField(null=True)
    tutor1 = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="tutor1")
    tutor2 = models.ForeignKey(Tutor2, on_delete=models.CASCADE, null=True)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE, related_name="tfgs")
    itineraries = models.ForeignKey(Itineraries, on_delete=models.CASCADE, null=True)
    mentions = models.ForeignKey(Mentions, on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField(Skills)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
         ordering = ['-createdAt']
