# pylint: disable=missing-docstring
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Cart
from .models import CartItem
from ..aggregation.models import checkout
from ..inventory.models import Inventory

def get_inventory(key):
    item = CartItem()
    inventory = Inventory.objects.get(id=key)
    item.id = key
    item.title = inventory.book.title
    item.status = inventory.status
    item.image = inventory.book.image
    return item

def cart_view(request):
    cart_items = []
    cart = Cart(request)
    for key in cart.keys():
        cart_items.append(get_inventory(key))
    return render(request, 'carts/view.html', {'items': cart_items})

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def cart_checkout(request):
    success, message = checkout(request)
    if success:
        return redirect('library')
    messages.error(request, message)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def cart_update(request):
    item_id = request.POST.get('inventory_id')

    if item_id is not None:
        cart = Cart(request)
        if 'add_to_cart' in request.POST:
            cart.add(item_id)
        if 'remove_from_cart' in request.POST:
            cart.remove(item_id)
        #cart.save()

        # request.session['cart_items'] = len(cart)
        # try:
        #     inventory_obj = Inventory.objects.get(id=item_id)
        # except inventory_obj.DoesNotExist:
        #     #messaage = "this item is not available."
        #     return redirect("library")
        # cart_obj = Cart.objects.new_or_get(request)
        # if inventory_obj in cart_obj.Items.all():
        #     cart_obj.Items.remove(inventory_obj)
        #     #added = False
        # else:
        #     cart_obj.Items.add(inventory_obj)
        #     #added = True

        # cart_id = request.session.get("cart_id", None)
        # cart_obj = Cart.objects.new(user=request.user)
        # request.session['cart_id'] = cart_obj.id
        # cart_obj.Items.add(item_id)
        # # request.session['cart_items'] = cart_id
        # request.session['cart_items'] = cart_obj.Items.count()

        # request.session['cart_items'] = request.session['cart_id']

    # if 'cart_items' in request.session:
    #     print(request.session.cart_items, flush=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))
