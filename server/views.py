# pylint: disable=missing-docstring
from django.shortcuts import render

def about_page(request):
    context = {
        "title":"About Page",
        "content":" Welcome to the about page."
    }
    return render(request, "about_page.html", context)
