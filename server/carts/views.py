# pylint: disable=missing-docstring
from django.shortcuts import redirect
from .models import Cart

#cart = Cart(request)

def cart_update(request):
    item_id = request.POST.get('inventory_id')

    if item_id is not None:
        cart = Cart(request)
        if 'add_to_cart' in request.POST:
            cart.add(item_id)
        # else:
        #     cart.remove(item_id)
            cart.save()

        request.session['cart_items'] = len(cart)
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
