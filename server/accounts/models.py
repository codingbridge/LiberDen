import uuid
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
#from server.membership.models import Membership, DiscountCoupon


class UserManager(BaseUserManager):
    def create_user(self, password=None, is_staff=False, is_active=True, **extra_fields):
        user = self.model(
            is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password=None, **extra_fields):
        return self.create_user(password, is_staff=True, is_superuser=True, **extra_fields)

    def customers(self):
        return self.get_queryset().filter(Q(is_staff=False))

    def staff(self):
        return self.get_queryset().filter(is_staff=True)

class Address(models.Model):
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    company_name = models.CharField(max_length=256, blank=True)
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    province = models.CharField(max_length=256, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

class User(AbstractBaseUser):
    email = models.EmailField()
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    addresses = models.ForeignKey(
        Address, related_name="+", null=True, blank=True
    )
    is_staff = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)
    note = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    shipping_address = models.ForeignKey(
        Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )
    # avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)
    # USERNAME_FIELD = "email"
    objects = UserManager()
