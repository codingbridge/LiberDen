from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from server.inventory.models import Inventory
from .models import Cart


def cart_update(request):
    item_id = request.POST.get('inventory_id')
    
    if item_id is not None:
        try:
            inventory_obj = Inventory.objects.get(id=item_id)
        except inventory_obj.DoesNotExist:
            #messaage = "this item is not available."
            return redirect("library")
        cart_obj = Cart.objects.new_or_get(request)
        if inventory_obj in cart_obj.Items.all():
            cart_obj.Items.remove(inventory_obj)
            #added = False
        else:
            cart_obj.Items.add(inventory_obj)
            #added = True
    
        request.session['cart_items'] = 10 #cart_obj.Items.count()


    # if 'cart_items' in request.session:
    #     print(request.session.cart_items, flush=True)
    return redirect("libray")
        
    #     if request.is_ajax(): # Asynchronous JavaScript And XML / JSON            
    #         json_data = {
    #             "added": added,
    #             "removed": not added,
    #             "cartItemCount": cart_obj.items.count()
    #         }
    #         return JsonResponse(json_data, status=200) 
    # return redirect("library")
