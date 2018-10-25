from django.urls import path
from .views import HomePageView, LoginPageView, ProjectPageView

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('login', LoginPageView.as_view(), name="login"),
    path('project', ProjectPageView.as_view(), name="project")
]