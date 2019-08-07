from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View, ListView, DetailView    
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Inventory
from .forms import DocumentForm


class LibraryView(ListView):
    template_name = "inventory/list.html"

    def get_queryset(self):
        if self.request.method == 'GET':            
            category = self.request.GET.get('q', None)            
            if category is None or not category.strip():
                whole = Inventory.objects.all()
            else:
                if ':' in category:
                    type, value = category.split(':')
                    whole = Inventory.objects.books_by_category(type, value)
                else:    
                    whole = Inventory.objects.books_by_category(None, category)
            # TODO: need to find a better solution, using annotate ?
            for item in whole:
                available_count = Inventory.objects.copies_count_by_id(item.book.id, 'A')
                unavailable_count = Inventory.objects.copies_count_by_id(item.book.id, 'N')
                item.available_count = available_count
                item.unavailable_count = unavailable_count
            return whole

    # def get_queryset(self, category):
    #     whole = Inventory.objects.all()
    #     # TODO: need to find a better solution, using annotate ?
    #     for item in whole:
    #         available_count = Inventory.objects.copies_count_by_id(item.book.id, 'A')
    #         unavailable_count = Inventory.objects.copies_count_by_id(item.book.id, 'N')
    #         item.available_count = available_count
    #         item.unavailable_count = unavailable_count
    #     return whole

    # def update_cart(self):
    #     self.request.session.cart_items = 1
    #     self.request.session.save()
    #     return redirect('Library')


def upload_form_view(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Upload')
    else:
        form = DocumentForm()
    return render(request, 'inventory/upload.html', {
        'form': form
    })
# def product_list_view(request):
#     queryset = Inventory.objects.all_available()
#     context = {
#         'object_list': queryset
#     }
#     return render(request, "inventory/list.html", context)
