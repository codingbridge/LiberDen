from django.shortcuts import render

def cart_update(request):
    item_id = request.POST.get('inventory_id')
    
    if item_id is not None:
        try:
            inventory_obj = Inventory.objects.get(id=item_id)
        except Product.DoesNotExist:
            messaage = "this item is not available."
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if inventory_obj in cart_obj.item.all():
            cart_obj.products.remove(inventory_obj)
            added = False
        else:
            cart_obj.items.add(inventory_obj)
            added = True
        request.session['cart_items'] = cart_obj.items.count()
        
        if request.is_ajax(): # Asynchronous JavaScript And XML / JSON            
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.items.count()
            }
            return JsonResponse(json_data, status=200) 
    return redirect("cart:home")
