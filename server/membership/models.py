from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models import Q
from server.book.models import TitleSlugModel, TraceModel


class Membership(TitleSlugModel, TraceModel):    
    price = models.DecimalField(max_digits=8, decimal_places=2)
#    valid_in_months = models.PositiveIntegerField()
    valid_in_days = models.PositiveIntegerField()
    max_book_count = models.PositiveIntegerField()
#    max_day_count = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Membership, self).save(*args, **kwargs)

class MembershipCard(TraceModel):
    membership = models.ForeignKey('Membership', on_delete=models.DO_NOTHING)
    is_valid_membership   = models.BooleanField(default=True)
    membership_activated_date = models.DateTimeField()
    membership_expiry_date = models.DateTimeField()

    def max_checkout_count(self, userid):
        cards = self.get_queryset().filter(Q(is_valid_membership=True) & Q(user__id=userid)).memebership_set
        for card in cards:
            count += card.max_book_count
        return count
