from django.urls import path
from .views import TfmListView

urlpatterns = [
    path('', TfmListView.as_view(), name="public_tfms_list"),
]