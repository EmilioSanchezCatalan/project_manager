from django.db import models

# Create your models here.
class Centers(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Departaments(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Areas(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Masters(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE)
    centers = models.ForeignKey(Centers, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Carrers(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE)
    centers = models.ForeignKey(Centers, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Mentions(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Itineraries(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Skills(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    text = models.TextField()
    itineraries = models.ForeignKey(Itineraries, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
