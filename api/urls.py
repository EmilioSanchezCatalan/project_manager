from django.urls import path
from api.views import ListItineraries, ListMentions, ListSkills, ListAreas

urlpatterns = [
    path('itineraries/<int:carrer_id>', ListItineraries.as_view(), name="api_itineraries"),
    path('mentions/<int:carrer_id>', ListMentions.as_view(), name="api_mentions"),
    path('skills/<int:itineraries_id>', ListSkills.as_view(), name="api_skills"),
    path('areas/<int:departaments_id>', ListAreas.as_view(), name="api_areas")
]