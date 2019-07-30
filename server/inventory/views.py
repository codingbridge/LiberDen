from django.shortcuts import render
from django.views.generic import View, ListView, DetailView    
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Inventory


class LibraryView(ListView):
    template_name = "inventory/list.html"
    def get_queryset(self):
        # request = self.request
        return Inventory.objects.all_available()

# def product_list_view(request):
#     queryset = Inventory.objects.all_available()
#     context = {
#         'object_list': queryset
#     }
#     return render(request, "inventory/list.html", context)