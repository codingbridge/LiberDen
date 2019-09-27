# pylint: disable=missing-docstring
from django.conf import settings
from django.db import models

USER = settings.AUTH_USER_MODEL

class TraceModel(models.Model):
    user = models.ForeignKey(USER, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TitleSlugModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)
    slug = models.CharField(max_length=255, unique=True, null=True, blank=True)
    slug_hash = models.CharField(max_length=32, unique=True, null=True, blank=True)

    class Meta:
        abstract = True

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Location(TitleSlugModel, TraceModel):
    pass
