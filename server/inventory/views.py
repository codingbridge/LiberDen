# pylint: disable=missing-docstring
import requests
from django.contrib import messages
from django.db import Error
from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Inventory, save_inventory
from .submodels.book import save_book, get_book
from .forms import DocumentForm

SESSION_BOOK = 'BOOK'
SESSION_INVENTORY = 'INVENTORY'
BOOK_DATA = {'title':"", 'description':"", 'pageCount':"", 'categories':"",
             'language':"", 'rating':"", 'author':"", 'publisher':"",
             'publishedDate':"", 'image': ""}
INVENTORY_DATA = {'bookid':"", 'title':"", 'description':"",
                  'isbn':"", 'price':"", 'call_number':""}

def get_book_data_form(request):
    return {
        'title': request.POST.get('title', None),
        'description': request.POST.get('description', None),
        'pageCount': request.POST.get('pageCount', None),
        'categories': request.POST.get('categories', None),
        'language': request.POST.get('language', None),
        'rating': request.POST.get('rating', None),
        'author': request.POST.get('author', None),
        'publisher': request.POST.get('publisher', None),
        'publishedDate': request.POST.get('publishedDate', None),
        'image':request.POST.get('image', None),
        }

def set_book_data_from_json(jsondata):
    data = BOOK_DATA
    if jsondata:
        data = {
            'title': jsondata['title'],
            'description': jsondata['description'],
            'pageCount': jsondata['pageCount'],
            'categories': ','.join(jsondata['categories']),
            'language': jsondata['language'],
            'rating': jsondata['averageRating'],
            'author': ', '.join(jsondata['authors']),
            'publisher': jsondata['publisher'],
            'publishedDate': jsondata['publishedDate'],
            'image': jsondata['imageLinks']['thumbnail']
            }
    return data

def set_inventory_data_from_book(book):
    data = {
        'bookid': str(book.id),
        'title': book.title,
        'description': book.description,
        'isbn': book.isbn,
        'price': "",
        'call_number':""
        # 'author': book.authors,
        # 'publisher': book.publisher,
        }
    return data

def fetch_google_isbn_api(isbn):
    # isbn = '9780545852500'
    if isbn:
        url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn
        response = requests.get(url)
        data = response.json()
    return data

@staff_member_required(login_url='login')
def book_add_view(request):
    isbn = ""
    data = BOOK_DATA
    if request.method == 'POST' and "search" in request.POST:
        isbn = request.POST.get('isbn', None)
        result = fetch_google_isbn_api(isbn)
        if result:
            data = set_book_data_from_json(result['items'][0]['volumeInfo'])
            request.session[SESSION_BOOK] = data
        else:
            messages.error(request, "couldn't find book data from google.")
    if request.method == 'POST' and "update" in request.POST:
        data = request.session.get(SESSION_BOOK)
        if not data:
            data = get_book_data_form(request)
        save_book(request.POST.get('isbn', None), data)
    return render(request, 'inventory/book.html', {'isbn': isbn, 'data': data})

@staff_member_required(login_url='login')
def inventory_add_view(request):
    isbn = ""
    data = INVENTORY_DATA
    if request.method == 'POST':
        isbn = request.POST.get('isbn', None)
        result = get_book(isbn)
        if result:
            data = set_inventory_data_from_book(result)
            request.session[SESSION_INVENTORY] = data
    if request.method == 'POST' and "update" in request.POST:
        data = request.session.get(SESSION_INVENTORY)
        data['price'] = request.POST.get('price', None)
        data['call_number'] = request.POST.get('call_number', None)
        try:
            save_inventory(data['bookid'], data)
        except Error as dberr:
            messages.error(request, dberr)
    return render(request, 'inventory/inventory.html', {'isbn': isbn, 'data': data})

def inventory_page_view(request):
    if request.method == 'GET':
        search = request.GET.get('q', None)
        items = Inventory.objects.books_search(search)
        for item in items:
            available_count = Inventory.objects.copies_count_by_id(item.book.id, 'A')
            unavailable_count = Inventory.objects.copies_count_by_id(item.book.id, 'N')
            item.available_count = available_count
            item.unavailable_count = unavailable_count
    return render(request, 'inventory/list.html', {'items': items})

@staff_member_required(login_url='login')
def upload_form_view(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Upload')
    else:
        form = DocumentForm()
    return render(request, 'inventory/upload.html', {'form': form})
