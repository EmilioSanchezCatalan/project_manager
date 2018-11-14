from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from login.models import Students
from .models import Tfms
from .forms import FilterPublicTfmForm, FilterTeacherTfmForm

class TfmListView(ListView):
    model = Tfms
    template_name = "tfms/public_tfms_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        # filtrar solo por aquellos que este validados completamente
        name = self.request.GET.get("name_project", "")
        master = self.request.GET.get("formation_project", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if master:
            queryset = queryset.filter(masters_id=master)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfms"
        context['form_filter'] = FilterPublicTfmForm(initial=self.request.GET.dict())
        return context

class TfmDetailView(DetailView):
    model = Tfms
    teamplate_name = "tfms/tfms_detail"

    # filtrar solo por aquellos que este validados completamente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfms_id=context['tfms'].id)
        context["back_url"] = "public_tfms_list"
        return context

class TeacherTfmListView(ListView):
    model = Tfms
    template_name = "tfms/teacher_tfms_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        name = self.request.GET.get("search_text", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfms"
        context['form_filter'] = FilterTeacherTfmForm(initial=self.request.GET.dict())
        context['nbar'] = "tfm"
        return context

class TeacherTfgDetailView(DetailView):
    model = Tfms
    teamplate_name = "tfms/tfms_detail"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfms_id=context['tfms'].id)
        context["back_url"] = "teacher_tfms_list"
        return context

class TeacherTfmDelete(RedirectView):
    url = "teacher_tfms_list"
    pattern_name = 'delete_Tfm'
    
    def get_redirect_url(self, *args, **kwargs):
        Tfms.objects.filter(id=kwargs['id'], tutor1=self.request.user).delete()
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url