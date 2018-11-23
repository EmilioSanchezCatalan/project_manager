from django.urls import path
from .views import LoginPageView, Logout

urlpatterns = [
    path('', LoginPageView.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout")
]