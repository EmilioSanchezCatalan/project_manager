from django.db import models
from core.models import Centers, Departaments, Areas
from tfgs.models import Tfgs
from tfms.models import Tfms

# Create your models here.
class Userinfos(models.Model):

    # Campos del modelo
    centers = models.ForeignKey(Centers, on_delete=models.CASCADE, null=True)
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE, null=True)
    areas = models.ForeignKey(Areas, on_delete=models.CASCADE, null=True)
    auth = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='userinfos')
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Students(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=255)
    dni = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    email = models.EmailField(max_length=150)
    tfgs = models.ForeignKey(Tfgs, on_delete=models.CASCADE, null=True, related_name="students")
    tfms = models.ForeignKey(Tfms, on_delete=models.CASCADE, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
