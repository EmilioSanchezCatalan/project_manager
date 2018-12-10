from django.db import models

# Create your models here.
class Centers(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150, verbose_name="Nombre")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = 'Centro'
        verbose_name_plural = 'Centros'

class Departaments(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150, verbose_name="Nombre")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

class Areas(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150, verbose_name="Nombre")
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE, related_name="areas", verbose_name="Departamento")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

class Masters(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150, verbose_name="Nombre")
    centers = models.ForeignKey(Centers, on_delete=models.CASCADE, related_name="masters", verbose_name="Centro de validación")
    departaments = models.ManyToManyField(Departaments, related_name="masters", verbose_name="Departamentos que imparten")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = 'Master'
        verbose_name_plural = 'Masters'


class Carrers(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150, verbose_name="Nombre")
    centers = models.ForeignKey(Centers, on_delete=models.CASCADE, related_name="carrers", verbose_name="Centro de validación")
    departaments = models.ManyToManyField(Departaments, related_name="carrers", verbose_name="Departamentos que imparten")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'
    

class Mentions(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150, verbose_name="Nombre")
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE, related_name="mentions", verbose_name="Titulación")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = 'Mencion'
        verbose_name_plural = 'Menciones'


class Itineraries(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150, verbose_name="Nombre")
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE, related_name="itineraries", verbose_name="Titulación")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Itinerario'
        verbose_name_plural = 'Itinerarios'


class Skills(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150, verbose_name="Iniciales")
    text = models.TextField(verbose_name="Descripción")
    itineraries = models.ForeignKey(Itineraries, on_delete=models.CASCADE, related_name="skills", verbose_name="Competencias")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name + ' - ' + self.text)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Competencia'
        verbose_name_plural = 'Competencias'


class Tutor2(models.Model):

    # Campos del modelo
    name = models.CharField(max_length=150, verbose_name="Nombre completo")
    departament = models.ForeignKey(Departaments, on_delete=models.CASCADE, verbose_name="Departamento")
    area = models.ForeignKey(Areas, on_delete=models.CASCADE, verbose_name="Area de conocimiento")
    curriculum_vitae = models.FileField(verbose_name="Curriculum", upload_to="cv", blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tutor de apoyo'
        verbose_name_plural = 'Tutores de apoyo'
