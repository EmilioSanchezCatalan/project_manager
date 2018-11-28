from django.contrib import admin
from .models import Centers, Departaments, Areas, Masters
from .models import Carrers, Mentions, Itineraries, Skills
from .models import Tutor2

class CentersAdmin(admin.ModelAdmin):
    pass

class DepartamentsAdmin(admin.ModelAdmin):
    pass

class AreasAdmin(admin.ModelAdmin):
    pass

class MastersAdmin(admin.ModelAdmin):
    pass

class CarrersAdmin(admin.ModelAdmin):
    pass

class MentionsAdmin(admin.ModelAdmin):
    pass

class ItinerariesAdmin(admin.ModelAdmin):
    pass

class SkillsAdmin(admin.ModelAdmin):
    pass

class Tutor2Admin(admin.ModelAdmin):
    pass

admin.site.register(Centers, CentersAdmin)
admin.site.register(Departaments, DepartamentsAdmin)
admin.site.register(Areas, AreasAdmin)
admin.site.register(Masters, MastersAdmin)
admin.site.register(Carrers, CarrersAdmin)
admin.site.register(Mentions, MentionsAdmin)
admin.site.register(Itineraries, ItinerariesAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(Tutor2, Tutor2Admin)