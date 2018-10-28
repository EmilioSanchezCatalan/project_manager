from django.urls import path
from .views import LoginPageView

urlpatterns = [
    path('', LoginPageView.as_view(), name="login")
]