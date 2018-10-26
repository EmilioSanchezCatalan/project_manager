from django.db import models

# Create your models here.
class Departaments(models.Model):
    name =  models.CharField(max_length=45)
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
    text = models.CharField(max_length=45)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Tutor2(models.Model):
    name = models.CharField(max_length=45)
    departament = models.CharField(max_length=45)
    area = models.CharField(max_length=45)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Students(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    dni = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    email = models.EmailField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Projects(models.Model):
    title = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField()
    mode = models.PositiveSmallIntegerField()
    is_team = models.BooleanField()
    objectives = models.TextField()
    methodology = models.TextField()
    docs_and_forms = models.TextField()
    language = models.CharField(max_length=45, null=True)
    knowledge = models.TextField(null=True)
    type_projects = models.PositiveSmallIntegerField()
    departament_validation = models.BooleanField()
    center_validation = models.BooleanField()
    tutor1 = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tutor2 = models.ForeignKey(Tutor2, on_delete=models.CASCADE, null=True)
    carrers = models.ForeignKey(Carrers, on_delete=models.CASCADE)
    itineraries = models.ForeignKey(Itineraries, on_delete=models.CASCADE, null=True)
    mentions = models.ForeignKey(Mentions, on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField(Skills)
    students = models.ManyToManyField(Students)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class Userinfos(models.Model):
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE)
    areas = models.ForeignKey(Areas, on_delete=models.CASCADE)
    auth = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")