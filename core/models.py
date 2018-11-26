from django.db import models

# Create your models here.
class Centers(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

class Departaments(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

class Areas(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE, related_name="areas")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

class Masters(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    centers = models.ForeignKey(Centers, on_delete=models.CASCADE, related_name="masters")
    departaments = models.ManyToManyField(Departaments, related_name="masters")
    departament = models.ForeignKey(Departaments, on_delete=models.CASCADE,  related_name="master")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

class Carrers(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    centers = models.ForeignKey(Centers, on_delete=models.CASCADE, related_name="carrers")
    departaments = models.ManyToManyField(Departaments, related_name="carrers")
    departament = models.ForeignKey(Departaments, on_delete=models.CASCADE,  related_name="carrer")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

class Mentions(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE, related_name="mentions")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

class Itineraries(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE, related_name="itineraries")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

class Skills(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    text = models.TextField()
    itineraries = models.ForeignKey(Itineraries, on_delete=models.CASCADE, related_name="skills")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name + ' - ' + self.text)
    
    class Meta:
         ordering = ['name']

class Tutor2(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150)
    departament = models.ForeignKey(Departaments, on_delete=models.CASCADE)
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
