import datetime
from django.db import models
# from django_mysql.models import ListTextField
# from book.models import Book
from inventory.models import Inventory
from customer.models import (Customer, Person)
from membership.models import Membership, DiscountCoupon

MAX_CHAR_LENGTH = 100
MAX_CHAR_LENGTH_MEMO = 500

'''
aggregate root:

visitor: 
book.listAll, book.listByCategory, book.search, book.AddToShoppingCart

login user:
book.listAll, book.listByCategory, book.search, book.AddToShoppingCart

profile.include(children).include(deliveryAddress)
.include(booklist).include(wishlist).include(requestlist).include(book-orderlist)
.include(book-overduelist).include(book-checkoutlist).include(book-borrow-history)
.include(membershiplist)

book.wishlistcount.readlistcount.favouritelistcount.include(inventory)

'''


class CustomerMembership(models.Model):
    customer = models.ManyToManyField('Customer')
    membership = models.ManyToManyField('Membership')
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    activate_date = models.DateField()

    def isExpired(self):
        return self.expiry_date > datetime.date.today()

# books that the customer has read
class CustomerBookReadList(models.Model):
    book = models.ManyToManyField('Inventory')
    customer = models.ManyToManyField('Customer')
    reader = models.ManyToManyField('Person')
    liked = models.BooleanField(default=False)
    rating = models.PositiveIntegerField()
    memo = models.CharField(max_length=MAX_CHAR_LENGTH_MEMO)
    create_datetime = models.DateTimeField(auto_now_add=True)

class CustomerBookRequestList(models.Model):
    book = models.ManyToManyField('Inventory')
    customer = models.ManyToManyField('Customer')
    reader = models.ManyToManyField('Person')
    expiry_date = models.DateField()
    create_datetime = models.DateTimeField(auto_now_add=True)

class CustomerBookOrderList(models.Model):
    book = models.ForeignKey('Inventory', on_delete=models.DO_NOTHING)
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    create_datetime = models.DateTimeField(auto_now_add=True)
    received_datetime = models.DateTimeField()
    received_by = models.ForeignKey('Staff', on_delete=models.DO_NOTHING)
    processed_datetime = models.DateTimeField()
    processed_by = models.ForeignKey('Staff', on_delete=models.DO_NOTHING)
    delivered_datetime = models.DateTimeField()
    delivered_by = models.ForeignKey('Courier', on_delete=models.DO_NOTHING)

    # is_fulfilled = models.BooleanField(default=False)
    # fullfill_datetime = models.DateTimeField()
    # fullfill_by = models.ForeignKey('Staff', on_delete=models.DO_NOTHING)
    
class Delivery(models.Model):
    pass