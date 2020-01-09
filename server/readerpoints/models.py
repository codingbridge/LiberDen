# pylint: disable=missing-docstring
import uuid
import datetime
from django.conf import settings
from django.db import models
from server.models import TraceModel
from server.users.models import UserProfile

USER = settings.AUTH_USER_MODEL

class PointsCardType(TraceModel):
    CATEGORY = (('G', 'Gold'), ('S', 'Silver'))
    EXPIRY_TYPE = (('Q', 'Quartly'), ('S', 'Semi-Annual'), ('A', 'Annual'))

    category = models.CharField(choices=CATEGORY, default='G', max_length=2)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    expiry_type = models.CharField(choices=EXPIRY_TYPE, default='A', max_length=2)
    expiry_num = models.PositiveIntegerField(default=1)
    is_retired = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.get_category_display()} ({self.quantity})'

class PointsCard(TraceModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_type = models.ForeignKey(PointsCardType, on_delete=models.CASCADE)
    activated_date = models.DateField(null=True, blank=True)
    puchased_date = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateField(null=True, blank=True)
    remain_quantity = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    holder = models.ForeignKey(USER, on_delete=models.CASCADE,
                               related_name="card_holder", null=True, blank=True)

    def __str__(self):
        return f'{self.card_type} - {self.holder} ({self.remain_quantity})'

    @property
    def is_valid(self):
        return not self.is_deleted and self.is_active and self.remain_quantity >= 0 \
        and self.expired_date <= datetime.date.today

# staff permission
def delete_card(cardid):
    try:
        card = PointsCard.objects.get(id=cardid)
        card.is_deleted = True
        card.save()
        return True
    except PointsCard.DoesNotExist:
        return False, f'Point Card is not found'
    except PointsCard.MultipleObjectsReturned:
        return False, f'Point Card has duplication.'

# staff permission
def deactivate_card(cardid):
    try:
        card = PointsCard.objects.get(card__id=cardid)
        card.is_active = False
        card.save()
        return True
    except PointsCard.DoesNotExist:
        return False, f'Point Card is not found'
    except PointsCard.MultipleObjectsReturned:
        return False, f'Point Card has duplication.'

# staff permission
def activate_card(cardid):
    try:
        card = PointsCard.objects.get(id=cardid)
        card.is_active = True
        card.save()
        return True
    except PointsCard.DoesNotExist:
        return False, f'Point Card is not found'
    except PointsCard.MultipleObjectsReturned:
        return False, f'Point Card has duplication.'

# staff or user permission
def puchase_card(cardtypeid, userid, isactivated):
    try:
        user_obj = UserProfile.objects.get(id=userid)
        cardtype_obj = PointsCardType.objects.get(id=cardtypeid, is_retired=False)

        card_obj = PointsCard()
        card_obj.card_type = cardtype_obj
        card_obj.puchased_date = datetime.datetime.now()
        card_obj.is_active = isactivated
        card_obj.holder = user_obj
        card_obj.save()
        return True
    except PointsCard.DoesNotExist:
        return False, f'Point Card is not found'
    except PointsCard.MultipleObjectsReturned:
        return False, f'Point Card has duplication.'
    except UserProfile.DoesNotExist:
        return False, f'User profile is not found'
    except UserProfile.MultipleObjectsReturned:
        return False, f'User profile has duplication.'

def get_cards(userid):
    return PointsCard.objects.get(holder__id=userid)

def get_default_card(userid):
    return get_cards(userid)[0]
