# from decimal import Decimal
# from django.conf import settings
# from django.db import models
# from django.db.models.signals import pre_save, post_save, m2m_changed
from server.inventory.models import Inventory

# def get_cart(request):
#     return request.session.get("cart", {})

# def add_to_cart(request, item_id):
#     cart = get_cart(request)
#     cart[item_id] = 1
#     request.session["cart"] = cart


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart", {})
        # if not cart:
        #     cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, itemid):
        # if itemid not in self.cart:
        self.cart[itemid]=1
        self.save()

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    def remove(self, itemid):
        if itemid in self.cart:
            del self.cart[itemid]
            self.save()

    def __len__(self):
        return sum(item for item in self.cart.values())

    def clear(self):
        del self.session["cart"]
        self.session.modified = True

# User = settings.AUTH_USER_MODEL

# class CartManager(models.Manager):
#     def new_or_get(self, request):
#         cart_id = request.session.get("cart_id", None)
#         qs = self.get_queryset().filter(id=cart_id)
#         if qs.count() == 1:
#             new_obj = False
#             cart_obj = qs.first()
#             #if request.user.is_authenticated() and cart_obj.user is None:
#             if cart_obj.user is None:
#                 cart_obj.user = request.user
#                 cart_obj.save()
#         else:
#             cart_obj = Cart.objects.new(user=request.user)
#             new_obj = True
#             request.session['cart_id'] = cart_obj.id
#         return cart_obj

#     def new(self, user=None):
#         user_obj = None
#         if user is not None:
#             #if user.is_authenticated():
#             user_obj = user
#         return self.model.objects.create(user=user_obj)

# class Cart(models.Model):
#     user     = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
#     Items    = models.ManyToManyField(Inventory, blank=True)
#     # subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
#     # total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
#     updated     = models.DateTimeField(auto_now=True)
#     timestamp   = models.DateTimeField(auto_now_add=True)

#     objects = CartManager()

#     def __str__(self):
#         return str(self.id)

# # def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
# #     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
# #         items = instance.items.all()
# #         total = 0
# #         for x in products:
# #             total += x.price
# #         if instance.subtotal != total:
# #             instance.subtotal = total
# #             instance.save()

# # m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)




# # def pre_save_cart_receiver(sender, instance, *args, **kwargs):
# #     if instance.subtotal > 0:
# #         instance.total = Decimal(instance.subtotal) * Decimal(1.08) # 8% tax
# #     else:
# #         instance.total = 0.00

# # pre_save.connect(pre_save_cart_receiver, sender=Cart)
