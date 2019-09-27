# pylint: disable=missing-docstring
from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)

