"""
    Configuración del panel de administración de la app.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.contrib import admin
from login.models import Userinfos, Students

class UserinfosAdmin(admin.ModelAdmin):
    pass

class StudentsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Userinfos, UserinfosAdmin)
admin.site.register(Students, StudentsAdmin)