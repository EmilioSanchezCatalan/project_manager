from django.views.generic.list import ListView
from core.models import Carrers
from .models import Tfgs

class TfgListView(ListView):
    model = Tfgs
    template_name = "core/public_project_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name_project", "")
        carrer = self.request.GET.get("formation_project", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if carrer:
            queryset = queryset.filter(carrers_id=carrer)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfgs"
        context['formations'] = Carrers.objects.all()
        context['default_select_value'] = "Titulación"
        context['filters'] = self.request.GET.dict()
        return context
