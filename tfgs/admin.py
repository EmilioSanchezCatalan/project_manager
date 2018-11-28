from django.contrib import admin
from .models import Tfgs

class TfgsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tfgs, TfgsAdmin)