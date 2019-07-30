from django.contrib import admin
from .models import Book, Author, Publisher, Category


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)