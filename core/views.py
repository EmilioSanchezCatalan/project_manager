from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginPageView(TemplateView):
    template_name = "core/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProjectPageView(TemplateView):
    template_name = "core/project.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)