import uuid
from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models import Q
from server.book.models import Book, TitleSlugModel, TraceModel

User = settings.AUTH_USER_MODEL

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# class InventoryQuerySet(models.QuerySet):
#     def availabe_copies(self):
#         return self.filter(Q(status='A'))

#     def copies_by_status(self, status_code):
#         return self.filter(Q(status=status_code))
    
#     def get_by_id(self, inventoryId):
#         return self.filter(Q(id=inventoryId))

#     def book(self, bookid):
#         return self.availabe_copies().filter(Q(book__id=bookid))

#     def books(self):
#         return self.availabe_copies().book_set.distinct()

#     def books_by_category(self, name, value):
#         return self.books().filter(Q(category__type=name) & Q(category__title=value)).distinct()

class InventoryManager(models.Manager):
    # def get_queryset(self):
    #     return InventoryQuerySet(self.model, using=self._db)
    
    # def all(self):
    #     return super().get_queryset().filter(~Q(status='R')).order_by("book")
    
    # def all_available(self):
    #     return super().get_queryset().filter(Q(status='A'))

    def copies_count_by_id(self, bookid, status_code):
        return super().get_queryset().filter(Q(book__id=bookid) & Q(status=status_code)).count()

    # def copies_count(self, status_code):
    #     return super().get_queryset().copies_by_status(status_code).count()

    # def book_copies(self, bookid):
    #     return super().get_queryset().book(bookid)

    # def book_copies_count(self, bookid):
    #     return super().get_queryset().book(bookid).count()

    # def books_count(self):
    #     return super().get_queryset().books().count()
    def get_name_value_pair(self, search):
        if ':' in search:
            name, value = search.split(':')
        else:
            name = None
            value = search
        
        return name, value

    def parse_search_string(self, search_string):
        search = {'name':None, 'value':None}
        search_string = search_string.lower()
        if '|' in search_string:
            sub_strings = search_string.split('|')
            for sub in sub_strings:
                name, value = get_name_value_pair(self, sub)
                search['name'] = name
                search['value'] = value
                #result = self.get_filtered_queryset(result, sub)
        else:
            #result = self.get_filtered_queryset(result, search_string)


        return search

    def get_broad_search_queryset(self):
        pass

    def is_like_isbn(self, str):
        pass   

    def search_by_name_value(self, queryset, name, value):
        if name == 'a':
            result = queryset.filter(Q(book__author__title__icontains=value))
        elif name == 'p':
            result = queryset.filter(Q(book__publisher__title__icontains=value))
        elif name == 'r':
            result = queryset.filter(Q(book__ranking=value))
        elif name == 'isbn':
            result = queryset.filter(Q(book__isbn=value))
        elif name == 'status':
            result = queryset.filter(Q(status=value))
        else:
            result = queryset.filter(Q(book__categories__type=name) & Q(book__categories__title=value))
        return result

    def get_filtered_queryset(self, queryset, search):
        if ':' in search:
            name, value = search.split(':')
        else:
            name = None
            value = search

        if name is None or not name.strip():
            result = queryset.filter(Q(book__title__icontains=value) | Q(book__sub_title__icontains=value))
        elif value is None or not value.strip():
            result = queryset.filter((Q(book__title__icontains=s) for s in name))
        else:
            result = self.search_by_name_value(queryset, name, value)

        return result

    def books_search(self, search_string):

        result = super().get_queryset().filter(~Q(status='R')).order_by("book")

        if search_string is None or not search_string.strip():
            return result

        search_string = search_string.lower()
        if '|' in search_string:
            sub_strings = search_string.split('|')
            for sub in sub_strings:
                result = self.get_filtered_queryset(result, sub)
        else:
            result = self.get_filtered_queryset(result, search_string)
                # name, value = sub.split(':')
                # if name is None or not name.strip():
                #     result = result.filter((Q(book__icontains=s) for s in value))
                # elif value is None or not value.strip():
                #     result = result.filter((Q(book__icontains=s) for s in name))
                # else:
                #     if name == 'a':
                #         result = result.filter(Q(book__author__title__icontains=value))
                #     elif name == 'p':
                #         result = result.filter(Q(book__publisher__title__icontains=value))
                #     elif name == 'r':
                #         result = result.filter(Q(book__ranking=value))
                #     elif name == 'isbn':
                #         result = result.filter(Q(book__isbn=value))
                #     elif name == 'status':
                #         result = result.filter(Q(status=value))
                #     else:
                #         result = result.filter(Q(book__categories__type=name) & Q(book__categories__title=value))

        return result
        
    # def books_by_category_count(self, name, value):
    #      return super().get_queryset().books_by_category(name, value).count()
    
    # def search(self, *args, **kwargs):
    #     pass

    # def is_available(self, inventoryid):
    #     pass

class Location(TitleSlugModel, TraceModel):
    pass

class Inventory(TraceModel):
    CURRENCY  = (('RMB', 'RMB'), ('USD', 'US Dollar'))    
    STATUS    = (('A', 'Available'), ('N', 'Not available'), ('R', 'Retired'))
    CONDITION = (('G', 'Good'), ('P', 'Poor'))

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book           = models.ForeignKey(Book, on_delete=models.CASCADE)
    price_amount   = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    price_currency = models.CharField(choices=CURRENCY, default='USD', max_length=3)
    acquired_date  = models.DateField(null=True, blank=True)
    retired_date   = models.DateField(null=True, blank=True)
    location       = models.ForeignKey('Location', on_delete=models.CASCADE, null=True, blank=True)
    condition      = models.CharField(choices=CONDITION, default='G', max_length=1)
    status         = models.CharField(choices=STATUS, default='A', max_length=1)    
    memo           = models.CharField(max_length=500, null=True, blank=True)
    call_number    = models.CharField(unique=True, max_length=20)

    objects = InventoryManager()

    def __str__(self):
        return self.book.title + ": " + self.book.sub_title

    @property
    def price(self):
        return f'{self.price_currency} {self.price_amount}'

    # class Meta:
    #     order_with_respect_to = 'book'

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
