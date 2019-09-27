# pylint: disable=missing-docstring
import datetime
from django.db import models
from server.models import TraceModel
from server.inventory.models import Inventory
from server.readerpoints.models import PointsCard


class Circulation(TraceModel):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    card = models.ForeignKey(PointsCard, on_delete=models.CASCADE)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    is_returned = models.BooleanField(default=False)
    memo = models.TextField(blank=True, null=True)

def borrow_a_book(bookid, cardid, memo):
    try:
        card_obj = PointsCard.objects.get(id=cardid)
        if card_obj.is_valid:
            inventory_obj = Inventory.objects.get(id=bookid)
            circulation_obj = Circulation()
            circulation_obj.inventory = inventory_obj
            circulation_obj.card = card_obj
            circulation_obj.borrowing_date = datetime.datetime.now
            if memo:
                circulation_obj.memo = memo
            circulation_obj.save()

            card_obj.remain_quantity -= 1
            card_obj.save()
            return True
    except PointsCard.objects.DoesNotExist:
        return False, f'User Points Card is not found.'
    except Inventory.objects.DoesNotExist:
        return False, f'Book is not found in the inventory.'

def return_a_book(bookid):
    try:
        circulation_obj = Circulation.objects.get(inventory__id=bookid)
        if circulation_obj.is_returned:
            circulation_obj.memo += f'Returned at {circulation_obj.return_date}|'
        circulation_obj.is_returned = True
        circulation_obj.return_date = datetime.datetime.now
        circulation_obj.save()

        card_obj = PointsCard.objects.get(id=circulation_obj.card.id)
        card_obj.remain_quantity += 1
        card_obj.save()
        return True
    except Circulation.objects.DoesNotExist:
        return False, f'Book is not found.'
    except PointsCard.objects.DoesNotExist:
        return False, f'User Points Card does not exist.'
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
'''