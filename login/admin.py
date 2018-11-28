from django.contrib import admin
from .models import Userinfos, Students

class UserinfosAdmin(admin.ModelAdmin):
    pass

class StudentsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Userinfos, UserinfosAdmin)
admin.site.register(Students, StudentsAdmin)