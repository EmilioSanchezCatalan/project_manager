"""
    Configuración de las urls de las vistas asociadas al login.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from django.urls import path
from login.views import LoginPageView, Logout
from login.views import PasswordResetForm, PasswordResetDone
from login.views import PasswordResetConfirm, PasswordResetComplete
from login.views import UserInfoUpdate

urlpatterns = [
    path('', LoginPageView.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('reset_email/', PasswordResetForm.as_view(), name="reset_email"),
    path('reset_done/', PasswordResetDone.as_view(), name="reset_done"),
    path('reset_confirm/<slug:uidb64>/<slug:token>', PasswordResetConfirm.as_view(), name="reset_confirm"),
    path('reset_complete/', PasswordResetComplete.as_view(), name="reset_complete"),
    path('userinfo/edit/<int:pk>/', UserInfoUpdate.as_view(), name="userinfo_edit")
]
