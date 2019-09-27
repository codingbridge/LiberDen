
# pylint: disable=missing-docstring
from django.contrib import admin
from .models import PointsCard, PointsCardType

admin.site.register(PointsCardType)
admin.site.register(PointsCard)
