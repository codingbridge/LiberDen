import uuid
from django.db import models
from book.models import Book

MAX_CHAR_LENGTH = 100
MAX_CHAR_LENGTH_DESCRIPTION = 200
MAX_CHAR_LENGTH_MEMO = 500


class Location(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)
    is_deleted = models.BooleanField(default=False)

class Condition(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)
    is_deleted = models.BooleanField(default=False)

class Status(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)
    is_deleted = models.BooleanField(default=False)

class Action(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)
    is_deleted = models.BooleanField(default=False)

class Currency(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    code = models.CharField(max_length=5)
    is_deleted = models.BooleanField(default=False)

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey('Book', on_delete=models.DO_NOTHING)
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_currency = models.ForeignKey('Currency', on_delete=models.DO_NOTHING)
    acquired_date = models.DateField()
    retired_date = models.DateField()
    location = models.ForeignKey('Location', on_delete=models.DO_NOTHING)
    condition = models.ForeignKey('Condition', on_delete=models.DO_NOTHING)
    status = models.ForeignKey('Status', on_delete=models.DO_NOTHING)
    action = models.ForeignKey('Action', on_delete=models.DO_NOTHING)
    memo = models.CharField(max_length=MAX_CHAR_LENGTH_MEMO)
    create_datetime = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_datetime = models.DateTimeField(null=True, blank=True)
