"""
    Configuración del panel de administración de la app.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.contrib import admin
from .models import AnnouncementsTfg

class AnnouncementsAdmin(admin.ModelAdmin):
    """
        Configuración especifica de las convocotorias.
    """
    pass


# Registro de los modelos en el panel administración.
admin.site.register(AnnouncementsTfg, AnnouncementsAdmin)
