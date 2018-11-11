from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from .forms import FilterPublicTfgForm, FilterTeacherTfgForm
from .models import Tfgs
from login.models import Students

class TfgListView(ListView):
    model = Tfgs
    template_name = "tfgs/public_tfgs_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name_project", "")
        carrer = self.request.GET.get("formation_project", "")
        print(name)
        if name:
            queryset = queryset.filter(title__contains=name)
        if carrer:
            queryset = queryset.filter(carrers_id=carrer)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = FilterPublicTfgForm(initial=self.request.GET.dict())
        return context

class TfgDetailView(DetailView):
    model = Tfgs
    teamplate_name = "tfgs/tfgs_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfgs_id=context['tfgs'].id)
        context["back_url"] = "public_tfgs_list"
        return context


class TeacherTfgListView(ListView):
    model = Tfgs
    template_name = "tfgs/teacher_tfgs_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        name = self.request.GET.get("search_text", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfgs"
        context['form_filter'] = FilterTeacherTfgForm(initial=self.request.GET.dict())
        context['nbar'] = "tfg"
        return context

class TeacherTfgDetailView(DetailView):
    model = Tfgs
    teamplate_name = "tfgs/tfgs_detail"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfgs_id=context['tfgs'].id)
        context["back_url"] = "teacher_tfgs_list"
        return context

class TeacherTfgDelete(RedirectView):
    url = "teacher_tfgs_list"
    pattern_name = 'delete_Tfm'
    
    def get_redirect_url(self, *args, **kwargs):
        Tfgs.objects.filter(id=kwargs['id']).delete()
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url