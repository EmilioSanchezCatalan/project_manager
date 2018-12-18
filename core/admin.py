"""
    Configuración del panel de administración de la app.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.contrib import admin
from .models import Centers, Departaments, Areas, Masters
from .models import Carrers, Mentions, Itineraries, Skills
from .models import Tutor2

class CentersAdmin(admin.ModelAdmin):

    """
        Clase destinada a la configuración del modelo Centers.
    """

    pass

class DepartamentsAdmin(admin.ModelAdmin):

    """
        Clase destinada a la configuración del modelo Departaments.
    """

    pass

class AreasAdmin(admin.ModelAdmin):

    """
        Clase destinada a la configuración del modelo Areas.
    """

    pass

class MastersAdmin(admin.ModelAdmin):

    """
        Clase destinada a la configuración del modelo Masters.
    """

    pass

class CarrersAdmin(admin.ModelAdmin):

    """
        Clase destinada a la configuración del modelo Carrers.
    """

    pass

class MentionsAdmin(admin.ModelAdmin):

    """
        Clase destinada a la configuración del modelo Mentions.
    """

    pass

class ItinerariesAdmin(admin.ModelAdmin):

    """
        Clase destinada a la configuración del modelo Itineraries.
    """

    pass

class SkillsAdmin(admin.ModelAdmin):

    """
        Clase destinada a la configuración del modelo Skills.
    """

    pass

class Tutor2Admin(admin.ModelAdmin):

    """
        Clase destinada a la configuración del modelo Tutor2.
    """

    pass


# Modelos registrados en el panel de administración.
admin.site.register(Centers, CentersAdmin)
admin.site.register(Departaments, DepartamentsAdmin)
admin.site.register(Areas, AreasAdmin)
admin.site.register(Masters, MastersAdmin)
admin.site.register(Carrers, CarrersAdmin)
admin.site.register(Mentions, MentionsAdmin)
admin.site.register(Itineraries, ItinerariesAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(Tutor2, Tutor2Admin)
