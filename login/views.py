from django.contrib.auth.views import LoginView
from django.urls import reverse

# Create your views here.
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
            