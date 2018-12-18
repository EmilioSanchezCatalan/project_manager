"""
    Configuración de las urls de las vistas asociadas a la home.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from django.urls import path
from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name="home")
]