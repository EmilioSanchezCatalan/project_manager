from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.shortcuts import render
from project.models import Tfgs

# Create your views here.
class HomePageView(TemplateView):
    template_name = "core/home.html"
