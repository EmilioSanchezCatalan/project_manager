from django.db import models
from core.models import Departaments, Areas

# Create your models here.
class Userinfos(models.Model):
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE)
    areas = models.ForeignKey(Areas, on_delete=models.CASCADE)
    auth = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")