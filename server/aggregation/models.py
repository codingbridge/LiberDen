# pylint: disable=missing-docstring
import datetime
from django.db import models
from django.contrib.auth.decorators import login_required
from server.models import TraceModel
from server.inventory.models import Inventory
from server.readerpoints.models import get_default_card
from server.readerpoints.models import PointsCard
from server.carts.models import Cart

class Circulation(TraceModel):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    card = models.ForeignKey(PointsCard, on_delete=models.CASCADE)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    is_returned = models.BooleanField(default=False)
    memo = models.TextField(blank=True, null=True)

@login_required
def assign_pointscardid_to_itemid(request):
    pass
    # get user's cards
    # cards = get_cards(request.user.userid)
    # if cards.count() == 1:
    #     value = cards.remain_quantity

    # cnt = 1
    # cart_object = Cart(request).cart
    # for key in cart_object.keys():
    #     card_object = cards[cnt]
    #     if card_object.remain_quantity > 0:
    #         cart_object.add(key, value)
    #         card_object.remain_quantity -= 1
    #     else:
    #         cnt += 1

@login_required
def checkout(request):
    try:
        cart = Cart(request)
        for key in cart.keys():
            #update inventory
            inventory = Inventory.objects.get(id=key)
            if inventory.status != 'A':
                cart.remove(key)
                continue
            inventory.status = 'N'
            inventory.save()
            card = get_default_card(request.userid)
            if card.remain_quantity >= 1:
                circulation_obj = Circulation()
                circulation_obj.inventory = inventory
                circulation_obj.card = card
                circulation_obj.borrowing_date = datetime.datetime.now
                # if memo:
                #     circulation_obj.memo = memo
                circulation_obj.save()

                card.remain_quantity -= 1
                card.save()
            else:
                pass
            #borrow_a_book(key, value, '')
            #cart_object.remove(key)
        cart.clear()
        return True, f''
    except PointsCard.objects.DoesNotExist:
        return False, f'User Points Card is not found.'
    except Inventory.objects.DoesNotExist:
        return False, f'Book is not found in the inventory.'
    except:
        return False, f'Failed to checkout.'

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

