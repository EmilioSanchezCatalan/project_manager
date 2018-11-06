from django.db import models
from core.models import Masters, Carrers, Itineraries, Mentions, Skills

# Create your models here.
class Tutor2(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    departament = models.CharField(max_length=150)
    area = models.CharField(max_length=150)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")


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
    departament_validation = models.BooleanField()
    center_validation = models.BooleanField()
    tutor1 = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tutor2 = models.ForeignKey(Tutor2, on_delete=models.CASCADE, null=True)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE)
    itineraries = models.ForeignKey(Itineraries, on_delete=models.CASCADE, null=True)
    mentions = models.ForeignKey(Mentions, on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField(Skills)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

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

class Students(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    dni = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    email = models.EmailField(max_length=150)
    tfgs = models.ForeignKey(Tfgs, on_delete=models.CASCADE, null=True)
    tfms = models.ForeignKey(Tfms, on_delete=models.CASCADE, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
