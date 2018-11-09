from django.views.generic.list import ListView
from .forms import FilterPublicTfgForm
from .models import Tfgs

class TfgListView(ListView):
    model = Tfgs
    template_name = "core/public_project_list.html"

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
        context['title'] = "Tfgs"
        context['form_filter'] = FilterPublicTfgForm(initial=self.request.GET.dict())
        return context
