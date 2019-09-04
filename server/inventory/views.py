import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .submodels.book import Save_Book, BOOK_DATA, Set_Book_Data
from .forms import DocumentForm


# class LibraryView(ListView):
#     template_name = "inventory/list.html"

#     def get_queryset(self):
#         if self.request.method == 'GET':            
#             search = self.request.GET.get('q', None)
#             whole = Inventory.objects.books_search(search)    
#             # TODO: need to find a better solution, using annotate ?
#             for item in whole:
#                 available_count = Inventory.objects.copies_count_by_id(item.book.id, 'A')
#                 unavailable_count = Inventory.objects.copies_count_by_id(item.book.id, 'N')
#                 item.available_count = available_count
#                 item.unavailable_count = unavailable_count
#             return whole

SESSION_NAME_BOOK = 'BOOK'

def fetch_google_isbn_api(isbn):
    # isbn = '9780545852500'
    if not isbn:
        return
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn
    response = requests.get(url)
    data = response.json()
    return data

def book_add_view(request):
    isbn = ""
    data = BOOK_DATA
    if request.method == 'POST' and "search" in request.POST:
        try:
            isbn = request.POST.get('isbn', None)
            result = fetch_google_isbn_api(isbn)
            if result:
                data = Set_Book_Data(result['items'][0]['volumeInfo'])
                request.session[SESSION_NAME_BOOK] = data
        except:
            pass
    if request.method == 'POST' and "update" in request.POST:
        Save_Book(request.POST.get('isbn', None), request.session.get(SESSION_NAME_BOOK))
    return render(request, 'book.html', {'isbn': isbn, 'data': data})

def inventory_page_view(request):
    if request.method == 'GET':            
        search = request.GET.get('q', None)
        items = Inventory.objects.books_search(search)    
        # TODO: need to find a better solution, using annotate ?
        for item in items:
            available_count = Inventory.objects.copies_count_by_id(item.book.id, 'A')
            unavailable_count = Inventory.objects.copies_count_by_id(item.book.id, 'N')
            item.available_count = available_count
            item.unavailable_count = unavailable_count        
        return render(request, 'inventory/list.html', { 'items': items })

def upload_form_view(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Upload')
    else:
        form = DocumentForm()
    return render(request, 'inventory/upload.html', { 'form': form })
