from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db import models, IntegrityError, transaction
from django.template.defaultfilters import slugify

User = settings.AUTH_USER_MODEL

class TraceModel(models.Model):
    user              = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_datetime  = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    class Meta:
       abstract = True

    def save(self, *args, **kwargs):
        super(TraceModel, self).save(*args, **kwargs)

class TitleSlugModel(models.Model):
    title       = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)
    slug        = models.CharField(max_length=255, unique=True, null=True, blank=True)
    slug_hash   = models.CharField(max_length=32, unique=True, null=True, blank=True)

    class Meta:
       abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slug = slugify(self.title)
        # self.slug_hash = hashlib.md5(self.slug).encode('utf-8').hexdigest()
        i = 0
        while True:
            try:
                savepoint = transaction.savepoint()
                res = super(TitleSlugModel, self).save(*args, **kwargs)
                transaction.savepoint_commit(savepoint)
                return res
            except IntegrityError:
                transaction.savepoint_rollback(savepoint)
                i += 1
                self.slug = '%s_%d' % (slug, i)

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Location(TitleSlugModel, TraceModel):
    pass


class CirculationManager(models.Manager):
    pass

class Circulation(TraceModel):
    STATUS = (('CO', 'Check out'), ('OH', 'On hold'), ('R', 'Return'), ('L', 'Lost'))
        
    inventory   = models.ForeignKey('Inventory', on_delete=models.DO_NOTHING)
    status      = models.CharField(choices=STATUS, max_length=3)
    expiry_days = models.PositiveSmallIntegerField()
    memo = models.TextField()
    is_completed        = models.BooleanField(default=False)
    handled_by  = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="Operator", null=True, blank=True)

    objects = CirculationManager()

    @property
    def checkedout_count(self, userid):
        return self.get_queryset().filter(Q(is_completed=False) & Q(user__id=userid) & Q(status='CO')).count()

    def checkedout(self, userid):
        return self.get_queryset().filter(Q(is_completed=False) & Q(user__id=userid) & Q(status='CO'))

    def onhold_count(self, userid):
        return self.get_queryset().filter(Q(is_completed=False) & Q(user__id=userid) & Q(status='OH')).count()

    def onhold(self, userid):
        return self.get_queryset().filter(Q(is_completed=False) & Q(user__id=userid) & Q(status='OH'))

    def overdue_count(self, userid):
        return self.get_queryset().filter(Q(is_completed=False) & Q(user__id=userid) & Q(status='CO') & 
                                          Q(datetime.now() - modified_datetime > expiry_days * 3600)).count()

    def overdue(self, userid):
        return self.get_queryset().filter(Q(is_completed=False) & Q(user__id=userid) & Q(status='CO') & 
                                          Q(datetime.now() - modified_datetime > expiry_days * 3600))

    def duesoon_count(self, userid):
        return self.get_queryset().filter(Q(is_completed=False) & Q(user__id=userid) & Q(status='CO') & 
                                          Q(datetime.now() - modified_datetime > (expiry_days - 3) * 3600)).count()

    def duesoon(self, userid):
        return self.get_queryset().filter(Q(is_completed=False) & Q(user__id=userid) & Q(status='CO') & 
                                          Q(datetime.now() - modified_datetime > (expiry_days - 3) * 3600))

    def onhold_total(self):
        return self.get_queryset().filter(Q(is_completed=False) & Q(status='OH'))

    def is_held_by_others(self, userid, inventoryid):
        return self.get_queryset().filter(Q(is_completed=False) & ~Q(user__id=userid) & 
                                          Q(status='OH') & Q(Inventory__id=inventoryid)).count() > 0

    def checkedout_history(self, userid):
        return self.get_queryset().filter(Q(is_completed=True) & Q(user__id=userid) & ~Q(status='CO') & ~Q(status='OH'))


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