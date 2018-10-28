from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
class LoginPageView(TemplateView):
    template_name = "login/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

