from django.urls import path
from .views import TfgListView

urlpatterns = [
    path('', TfgListView.as_view(), name="public_tfgs_list"),
]