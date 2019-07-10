from django.db import models

MAX_CHAR_LENGTH = 100
MAX_CHAR_LENGTH_MEMO = 500


class Membership(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    valid_in_months = models.PositiveIntegerField()
    valid_in_days = models.PositiveIntegerField()
    allow_book_count = models.PositiveIntegerField()
    allow_day_count = models.PositiveIntegerField()
    memo = models.CharField(max_length=MAX_CHAR_LENGTH_MEMO)
    create_datetime = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_datetime = models.DateTimeField(null=True, blank=True)

class DiscountCoupon(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    code = models.CharField(max_length=MAX_CHAR_LENGTH)
    memo = models.CharField(max_length=MAX_CHAR_LENGTH_MEMO)
    create_datetime = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_datetime = models.DateTimeField(null=True, blank=True)
