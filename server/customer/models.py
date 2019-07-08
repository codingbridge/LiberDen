from django.db import models
import datetime

MAX_CHAR_LENGTH = 100


class Customer(models.Model):
    # user
    full_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    mobile_phone = models.CharField(max_length=MAX_CHAR_LENGTH)
    email_address = models.EmailField()
    nick_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    #reading_level = models.CharField(max_length=MAX_CHAR_LENGTH)
    #school_grade = models.CharField(max_length=MAX_CHAR_LENGTH)
    #school_type = models.CharField(max_length=MAX_CHAR_LENGTH)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE)
    delivery_address = models.CharField()
    delivery_phone = models.CharField(max_length=MAX_CHAR_LENGTH)
    delivery_contact_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True)

class CustomerBook(models.Model):
    pass

class CustomerMembership(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    card_type = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    activate_date = models.DateField()

    def isExpired(self):
        return self.expiry_date > datetime.date.today()

class Membership(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    valid_num_month = models.PositiveIntegerField()
    allow_num_book_rental = models.PositiveIntegerField()
    allow_num_day_rental = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True)

class DiscountCoupon(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    code = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True)

