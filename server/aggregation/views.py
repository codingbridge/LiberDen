# pylint: disable=missing-docstring

from django.shortcuts import render
from server.carts.models import Cart
from server.inventory.models import Inventory
from server.readerpoints.models import get_cards

CART_DATA = [{'id': "", 'title':""}]
POINTSCARD_DATA = [{'id':"", 'title':"", 'quantity':""}]

def show_cart(request):
    cart_obj = Cart(request).cart
    for k, v in cart_obj.items():
        book_obj = Inventory.objects.get(id=k)
        CART_DATA.append(k, book_obj.book.title)
    if request.user.is_authenticated:
        cards = get_cards(request.user.id)
        for card in cards:
            POINTSCARD_DATA.append(card.id, card.title, card.remain_quantity)
    else:
        pass
    return render(request, 'aggregation/shoppingcart.html',
                  {
                      'items': CART_DATA,
                      'cards': POINTSCARD_DATA})
