"""
    Configuración del panel de administración de la app.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.contrib import admin
from .models import Tfms

class TfmsAdmin(admin.ModelAdmin):
    
    """
        Clase destinada a la configuración del modelo Tfgs.
    """

    pass


# Modelos registrados en el panel de administración.
admin.site.register(Tfms)