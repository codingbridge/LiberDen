from django.db import models
from book.models import Book
from inventory.models import Inventory
from customer.models import (Customer, Child)
from membership.models import Membership, DiscountCoupon

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


# books that the customer has read
class CustomerBookReadList(models.Model):
    book = models.ForeignKey('Inventory', on_delete=models.DO_NOTHING)
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    child = models.ForeignKey('Child', on_delete=models.DO_NOTHING)
    rating = models.PositiveIntegerField()
    memo = models.CharField(max_length=MAX_CHAR_LENGTH_MEMO)
    create_datetime = models.DateTimeField(auto_now_add=True)

class CustomerBookFavouriteList(models.Model):
    book = models.ForeignKey('Book', on_delete=models.DO_NOTHING)
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    create_datetime = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

class CustomerBookRequestList(models.Model):
    book = models.ForeignKey('Inventory', on_delete=models.DO_NOTHING)
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    expiry_date = models.DateField()
    create_datetime = models.DateTimeField(auto_now_add=True)

class CustomerBookWishList(models.Model):
    book = models.ForeignKey('Book', on_delete=models.DO_NOTHING)
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    create_datetime = models.DateTimeField(auto_now_add=True)

class CustomerBookOrderList(models.Model):
    book = models.ForeignKey('Book', on_delete=models.DO_NOTHING)
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