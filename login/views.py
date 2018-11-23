from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy

class LoginPageView(LoginView):
    template_name = "login/login.html"
    redirect_authenticated_user = True

    def get_redirect_url(self):
        if self.request.user.is_staff:
            return reverse('admin:index')
        if self.request.user.groups.filter(id=1).exists():
            return reverse('teacher_tfgs_list')
        elif self.request.user.groups.filter(id=2).exists():
            return reverse('public_tfgs_list')
        elif self.request.user.groups.filter(id=3).exists():
            return reverse('public_tfgs_list')
        else: 
            return reverse('home')

@method_decorator(login_required, name='dispatch')
class Logout(RedirectView):
    url = reverse_lazy("login")
    pattern_name = 'logout'
    
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        url = super().get_redirect_url(*args, **kwargs)
        return url
            