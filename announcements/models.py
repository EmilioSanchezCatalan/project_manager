from django.db import models
from core.models import Centers

class Announcements(models.Model):

    STATUS_OPEN = 0
    STATUS_TEXT_OPEN = "Abierta para proponer"
    STATUS_PUBLIC = 1
    STATUs_TEXT_PUBLIC = "Abierta para solucitudes"
    STATUS_CLOSE = 2
    STATUS_TEXT_CLOSE = "Cerrada"
    STATUS_CHOICE = (
        (STATUS_OPEN, STATUS_TEXT_OPEN),
        (STATUS_PUBLIC, STATUs_TEXT_PUBLIC),
        (STATUS_CLOSE, STATUS_TEXT_CLOSE)
    )

    #Campos del modelo
    name = models.CharField(max_length=255, verbose_name="Nombre")
    status = models.PositiveSmallIntegerField(verbose_name="Estado de la convocatoria", choices=STATUS_CHOICE)
    centers = models.ForeignKey(Centers, on_delete=models.CASCADE, related_name="announcements", verbose_name="Centro")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")