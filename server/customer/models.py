import uuid
import datetime
from django.db import models
from django_mysql.models import ListTextField
from book.models import Book
from inventory.models import Inventory

MAX_CHAR_LENGTH = 100
MAX_CHAR_LENGTH_MEMO = 500


class Customer(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user
    full_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    mobile_phone = models.CharField(max_length=MAX_CHAR_LENGTH)
    email_address = models.EmailField()
    display_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    delivery_address = models.CharField(max_length=MAX_CHAR_LENGTH)
    delivery_phone = models.CharField(max_length=MAX_CHAR_LENGTH)
    delivery_contact_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    memo = models.CharField(max_length=MAX_CHAR_LENGTH_MEMO)
    create_datetime = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_datetime = models.DateTimeField(null=True, blank=True)

class Child(models.Model):
    full_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    display_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    reading_level = models.CharField(max_length=MAX_CHAR_LENGTH)
    school_grade = models.CharField(max_length=MAX_CHAR_LENGTH)
    school_type = models.CharField(max_length=MAX_CHAR_LENGTH)
    school_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    parent = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    is_deleted = models.BooleanField(default=False)
    deleted_datetime = models.DateTimeField(null=True, blank=True)


class CustomerMembership(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    membership = models.ForeignKey('Membership', on_delete=models.DO_NOTHING)
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    activate_date = models.DateField()

    def isExpired(self):
        return self.expiry_date > datetime.date.today()
