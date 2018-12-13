from django.contrib import admin
from .models import AnnouncementsTfg

class AnnouncementsAdmin(admin.ModelAdmin):
    pass

admin.site.register(AnnouncementsTfg, AnnouncementsAdmin)