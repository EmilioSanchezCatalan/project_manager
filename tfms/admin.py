from django.contrib import admin
from .models import Tfms

class TfmsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tfms)