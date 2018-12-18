"""
    Modelos de la app announcements.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from django.db import models
from core.models import Centers

class AnnouncementsTfg(models.Model):

    """
        Modelo donde guardar la información de las convocatorias de TFGs
    """

    STATUS_OPEN = 0
    STATUS_TEXT_OPEN = "Abierta para proponer"
    STATUS_PUBLIC = 1
    STATUS_TEXT_PUBLIC = "Abierta para solucitudes"
    STATUS_CLOSE = 2
    STATUS_TEXT_CLOSE = "Cerrada"
    STATUS_CHOICE = (
        (STATUS_OPEN, STATUS_TEXT_OPEN),
        (STATUS_PUBLIC, STATUS_TEXT_PUBLIC),
        (STATUS_CLOSE, STATUS_TEXT_CLOSE)
    )

    #Campos del modelo
    name = models.CharField(max_length=255, verbose_name="Nombre")
    status = models.PositiveSmallIntegerField(
        verbose_name="Estado de la convocatoria",
        choices=STATUS_CHOICE
    )
    centers = models.ForeignKey(
        Centers,
        on_delete=models.CASCADE,
        related_name="announcementstfg",
        verbose_name="Centro"
    )
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

class AnnouncementsTfm(models.Model):

    """
        Modelo destinado a guardar la información de covocatorias de TFMs
    """

    STATUS_OPEN = 0
    STATUS_TEXT_OPEN = "Abierta para proponer"
    STATUS_PUBLIC = 1
    STATUS_TEXT_PUBLIC = "Abierta para solicitudes"
    STATUS_CLOSE = 2
    STATUS_TEXT_CLOSE = "Cerrada"
    STATUS_CHOICE = (
        (STATUS_OPEN, STATUS_TEXT_OPEN),
        (STATUS_PUBLIC, STATUS_TEXT_PUBLIC),
        (STATUS_CLOSE, STATUS_TEXT_CLOSE)
    )

    #Campos del modelo
    name = models.CharField(max_length=255, verbose_name="Nombre")
    status = models.PositiveSmallIntegerField(
        verbose_name="Estado de la convocatoria",
        choices=STATUS_CHOICE
    )
    centers = models.ForeignKey(
        Centers,
        on_delete=models.CASCADE,
        related_name="announcementstfm",
        verbose_name="Centro"
    )
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")