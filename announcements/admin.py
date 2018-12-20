"""
    Configuración del panel de administración de la app.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.contrib import admin
from announcements.models import AnnouncementsTfg, AnnouncementsTfm

class AnnouncementsTfgAdmin(admin.ModelAdmin):
    """
        Configuración especifica de las convocotorias.
    """
    pass

class AnnouncementsTfmAdmin(admin.ModelAdmin):
    """
        Configuración especifica de las convocotorias.
    """
    pass


# Registro de los modelos en el panel administración.
admin.site.register(AnnouncementsTfg, AnnouncementsTfgAdmin)
admin.site.register(AnnouncementsTfm, AnnouncementsTfmAdmin)
