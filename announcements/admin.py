from django.contrib import admin
from .models import Announcements

class AnnouncementsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Announcements, AnnouncementsAdmin)