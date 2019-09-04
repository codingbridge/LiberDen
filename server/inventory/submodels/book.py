import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from .common import TitleSlugModel, TraceModel

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
    value = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.type + ":" + self.title

class Country(TitleSlugModel, TraceModel):    
    code = models.CharField(max_length=5)
    
    def __str__(self):
        return self.title

class Author(TitleSlugModel, TraceModel):
    full_name = 'title'
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING, null=True, blank=True)
    mailing_address = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.title

class Publisher(TitleSlugModel, TraceModel):
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING, null=True, blank=True)
    mailing_address = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.title

class Book(TitleSlugModel, TraceModel):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn         = models.CharField(max_length=30)
    sub_title    = models.CharField(max_length=200, null=True, blank=True)
    publisher    = models.ForeignKey('Publisher', on_delete=models.DO_NOTHING, null=True, blank=True)
    description  = models.TextField(null=True, blank=True)
    memo         = models.CharField(max_length=500, null=True, blank=True)
    word_count   = models.PositiveIntegerField(null=True, blank=True)
    page_count   = models.PositiveIntegerField(null=True, blank=True)
    ranking      = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(9)], null=True, blank=True)
    categories   = models.ManyToManyField('Category')
    authors      = models.ManyToManyField('Author')
    image        = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title + ": " + self.sub_title

def Save_Book(isbn, data):
    try:
        try:
            obj = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            book = Book()
            book.isbn = isbn
            book.title = data['title']
            book.description = data['description']
            book.page_count = int(data['pageCount'])
            book.ranking = int(float(data['rating']) * 2)
            publisher_obj, created = Publisher.objects.get_or_create(title=data['publisher'])
            book.publisher = publisher_obj
            filepath = Save_Image(data['image'], isbn + ".jpg")
            book.image = filepath
            book.save()
            authors=data['author'].split(",")
            for auth in authors:
                author_obj, created = Author.objects.get_or_create(title=auth)
                book.authors.add(author_obj)
            language_obj, created = Category.objects.get_or_create(
                type='L', title=data['language'])
            genres_obj, created = Category.objects.get_or_create(
                type='G', title=data['categories'])
            book.categories.add(language_obj, genres_obj)
    except Exception as e:
        print(e)

BOOK_DATA = {'title':"", 'description':"", 'pageCount':"", 'categories':"", 
'language':"", 'rating':"", 'author':"", 'publisher':"", 'publishedDate':"", 'image': ""}

def Set_Book_Data(jsonData):
    data = BOOK_DATA
    try:
        data = {
                'title': jsonData['title'],
                'description': jsonData['description'],
                'pageCount': jsonData['pageCount'],
                'categories': ','.join(jsonData['categories']),
                'language': jsonData['language'],
                'rating': jsonData['averageRating'],
                'author': ', '.join(jsonData['authors']),
                'publisher': jsonData['publisher'],
                'publishedDate': jsonData['publishedDate'],
                'image': jsonData['imageLinks']['thumbnail']
                }
    except:
        pass
    return data

def Save_Image(imgUrl, fileName):
    filepath=settings.MEDIA_ROOT + '\\images\\' + fileName
    try:        
        with open(filepath, 'wb') as handle:
            img_data = requests.get(imgUrl, stream=True)
            if not img_data:
                pass
            for block in img_data.iter_content(1024):
                if not block:
                    break
                handle.write(block)
    except:
        pass
    return settings.MEDIA_URL + 'image/' + fileName