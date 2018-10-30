from django.db import models

# Create your models here.
class Departaments(models.Model):
    name = models.CharField(max_length=45)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Areas(models.Model):
    name = models.CharField(max_length=45)
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Carrers(models.Model):
    name = models.CharField(max_length=45)
    areas = models.ForeignKey(Areas, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Mentions(models.Model):
    name = models.CharField(max_length=45)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Itineraries(models.Model):
    name = models.CharField(max_length=45)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Skills(models.Model):
    text = models.TextField()
    itineraries = models.ForeignKey(Itineraries, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
