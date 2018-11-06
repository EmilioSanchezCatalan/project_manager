from django.db import models
from core.models import Centers, Departaments, Areas

# Create your models here.
class Userinfos(models.Model):

    # Campos del modelo
    centers = models.ForeignKey(Centers, on_delete=models.CASCADE, null=True)
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE, null=True)
    areas = models.ForeignKey(Areas, on_delete=models.CASCADE, null=True)
    auth = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
