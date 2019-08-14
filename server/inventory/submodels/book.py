import uuid
from django.db import models
from django.core.validators import MaxValueValidator
from server.inventory.submodels.common import TitleSlugModel, TraceModel

class Category(TitleSlugModel, TraceModel):
    CATEGORY_TYPE = (
        ('AR', 'ArPoints'),
        ('AT', 'ATOS book level'),
        ('C', 'Cover type'),
        ('G', 'Genres'), 
        ('IL', 'Interest level'),
        ('L', 'Language'),
        ('LL', 'Lexile level'),
        ('RL', 'Reading level'),
        ('QN', 'Quiz number'),
        ('S', 'Subject'),
        ('SE', 'Series')
    )
    type = models.CharField(max_length=3, choices=CATEGORY_TYPE)
    level = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.type + ":" + self.title
    
    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)

class Country(TitleSlugModel, TraceModel):    
    code = models.CharField(max_length=5)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Country, self).save(*args, **kwargs)

class Author(TitleSlugModel, TraceModel):
    full_name = 'title'
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING, null=True, blank=True)
    mailing_address = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Author, self).save(*args, **kwargs)

class Publisher(TitleSlugModel, TraceModel):
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING, null=True, blank=True)
    mailing_address = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Publisher, self).save(*args, **kwargs)

class Book(TitleSlugModel, TraceModel):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn         = models.CharField(max_length=30)
    sub_title    = models.CharField(max_length=200, null=True, blank=True)
    author       = models.ForeignKey('Author', on_delete=models.DO_NOTHING)
    publisher    = models.ForeignKey('Publisher', on_delete=models.DO_NOTHING, null=True, blank=True)
    description  = models.TextField(null=True, blank=True)
    memo         = models.CharField(max_length=500, null=True, blank=True)
    word_count   = models.PositiveIntegerField(null=True, blank=True)
    page_count   = models.PositiveIntegerField(null=True, blank=True)
    ranking      = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(9)], null=True, blank=True)
    categories   = models.ManyToManyField('Category')
    image        = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title + ": " + self.sub_title

    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)

    # class Meta:
    #     ordering = ['-title', '-sub_title', '-id']
