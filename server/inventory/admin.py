# pylint: disable=missing-docstring
from django.contrib import admin
from .models import Inventory
from .submodels.book import Book, Author, Publisher, Category

admin.site.register(Inventory)
#admin.site.register(Location)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
