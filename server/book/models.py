import uuid
import hashlib
from django.conf import settings
from django.db import models, IntegrityError, transaction
from django.core.validators import MaxValueValidator
from django.template.defaultfilters import slugify

User = settings.AUTH_USER_MODEL


class TraceModel(models.Model):
    user              = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_datetime  = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    #is_deleted        = models.BooleanField(default=False)

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
