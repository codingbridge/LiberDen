import uuid
from django.db import models
from django.db.models import Q
from .submodels.book import Book
from .submodels.common import TitleSlugModel, TraceModel, Location, Document
from .utils import get_search_keywords_dict


class InventoryManager(models.Manager):
    def copies_count_by_id(self, bookid, status_code):
        return super().get_queryset().filter(Q(book__id=bookid) & Q(status=status_code)).count()

    def get_broad_search_queryset(self):
        pass

    def is_like_isbn(self, str):
        pass   

    def search_by_name_value(self, queryset, name, value):
        if name == 'a' or name.lower() == 'author':
            result = queryset.filter(Q(book__author__title__icontains=value))
        elif name == 'p' or name.lower() == 'publisher':
            result = queryset.filter(Q(book__publisher__title__icontains=value))
        elif name == 'r' or name.lower() == 'ranking':
            result = queryset.filter(Q(book__ranking=value))
        elif name == 'isbn':
            result = queryset.filter(Q(book__isbn=value))
        elif name == 'status':
            result = queryset.filter(Q(status=value))
        elif name == 'title':
             result = queryset.filter(Q(book__title__icontains=value))
        elif name == 'subtitle':
            result = queryset.filter(Q(book__sub_title__icontains=value))
        elif name == 'description':
            result = queryset.filter(Q(book__description__icontains=value))
        elif name == '': #title, subtitle
            result = queryset.filter(Q(book__title__icontains=value) | Q(book__sub_title__icontains=value))
        else: #categories
            result = queryset.filter(Q(book__categories__type=name) & Q(book__categories__title=value))
        return result

    def books_search(self, search_string):
        result = super().get_queryset().filter(~Q(status='R')).order_by("book")

        if search_string is None or not search_string.strip():
            return result

        pairs = get_search_keywords_dict(search_string.lower())
        for p in pairs:
            for v in pairs[p]:
                result = self.search_by_name_value(result, p, v)

        return result


class Inventory(TraceModel):
    CURRENCY  = (('RMB', 'RMB'), ('USD', 'US Dollar'))    
    #STATUS    = (('A', 'Available'), ('N', 'Not available'), ('R', 'Retired'))
    CONDITION = (('G', 'Good'), ('P', 'Poor'))
    LOAN_STATUS = [
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    ]

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book           = models.ForeignKey(Book, on_delete=models.CASCADE)
    price_amount   = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    price_currency = models.CharField(choices=CURRENCY, default='USD', max_length=3)
    acquired_date  = models.DateField(null=True, blank=True)
    retired_date   = models.DateField(null=True, blank=True)
    location       = models.ForeignKey('Location', on_delete=models.CASCADE, null=True, blank=True)
    condition      = models.CharField(choices=CONDITION, default='G', max_length=1)
    status         = models.CharField(choices=LOAN_STATUS, default='A', max_length=1)    
    memo           = models.CharField(max_length=500, null=True, blank=True)
    call_number    = models.CharField(unique=True, max_length=20)
    is_retired     = models.BooleanField(default=False)
    # due_back       = models.DateField(null=True, blank=True)

    objects = InventoryManager()

    def __str__(self):
        return self.book.title + ": " + self.book.sub_title

    @property
    def price(self):
        return f'{self.price_currency} {self.price_amount}'

def Save_Inventory():
    pass