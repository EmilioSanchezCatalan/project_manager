from django.db import models
from core.models import Centers, Departaments, Areas
from tfgs.models import Tfgs
from tfms.models import Tfms

# Create your models here.
class Userinfos(models.Model):

    # Campos del modelo
    centers = models.ForeignKey(Centers, on_delete=models.CASCADE, null=True, verbose_name="Centro", blank=True)
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE, null=True, verbose_name="Departamento", blank=True)
    areas = models.ForeignKey(Areas, on_delete=models.CASCADE, null=True, verbose_name="Area", blank=True)
    auth = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='userinfos', verbose_name="Usuario")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.auth)
    
    class Meta:
        verbose_name = 'Información de usuario'
        verbose_name_plural = 'Informaciones de usuario'

class Students(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=255, verbose_name="Nombre completo")
    dni = models.CharField(max_length=45, verbose_name="Dni")
    phone = models.CharField(max_length=45, verbose_name="Teléfono")
    email = models.EmailField(max_length=150, verbose_name="E-mail")
    tfgs = models.ForeignKey(Tfgs, on_delete=models.CASCADE, null=True, related_name="students", verbose_name="Trabajo fin de grado", blank=True)
    tfms = models.ForeignKey(Tfms, on_delete=models.CASCADE, null=True, related_name="students", verbose_name="Trabajo fin de master", blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'