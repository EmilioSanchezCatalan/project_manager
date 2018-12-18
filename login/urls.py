"""
    Configuración de las urls de las vistas asociadas al login.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from django.urls import path
from .views import LoginPageView, Logout

urlpatterns = [
    path('', LoginPageView.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout")
]