"""
    Controladores de la vistas login

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from django.views.generic.base import RedirectView
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from login.forms import ResetEmailForm, ResetPasswordForm

class LoginPageView(LoginView):

    """
        Controlador de la vista principal

        Atributos:
            template_name(str): template donde renderizar la vista login
            redirect_authenticated_user: activa la redirección de usuario
    """

    template_name = "login/login.html"
    redirect_authenticated_user = True

    def get_redirect_url(self):
        if self.request.user.is_staff:
            return reverse('admin:index')
        if self.request.user.groups.filter(name="Teachers").exists():
            return reverse('teacher_tfgs_list')
        if self.request.user.groups.filter(name="Departaments").exists():
            return reverse('departament_tfgs_list')
        if self.request.user.groups.filter(name="Centers").exists():
            return reverse('announ_tfgs_list')
        return reverse('home')

@method_decorator(login_required, name='dispatch')
class Logout(RedirectView):

    """
        Controlador para el cierre de sesión de usuarios.

        Atributos:
            url(str): dirección url de la redirección
            pattern_name(str): TODO explicar
    """

    url = reverse_lazy("login")
    pattern_name = 'logout'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        url = super().get_redirect_url(*args, **kwargs)
        return url

class PasswordResetForm(PasswordResetView):

    """
        Controlador para resetear la contraseña a traves del correo
        electrónico
    """

    template_name = "login/password_reset_form.html"
    email_template_name = "login/password_reset_email.html"
    success_url = reverse_lazy("reset_done")
    extra_context = {'form': ResetEmailForm}

class PasswordResetDone(PasswordResetDoneView):

    """
        Controlador que confirma el inicio del reseteo de contraseña
    """

    template_name = "login/password_reset_done.html"

class PasswordResetConfirm(PasswordResetConfirmView):

    """
        Controlador donde se establece la nueva contraseña del usuario.
    """

    template_name = "login/password_reset_confirm.html"
    success_url = reverse_lazy("reset_complete")
    extra_context = {'form': ResetPasswordForm}

class PasswordResetComplete(PasswordResetCompleteView):

    """
        Controlador que confirma que la contraseña a sido modificada
        correctamente.
    """

    template_name = "login/password_reset_complete.html"
