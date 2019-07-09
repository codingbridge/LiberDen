from django.db import models
from django_mysql.models import ListTextField

MAX_CHAR_LENGTH = 100
MAX_CHAR_LENGTH_DESCRIPTION = 200
MAX_CHAR_LENGTH_MEMO = 500

class Country(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    other_name = models.CharField(max_length=MAX_CHAR_LENGTH)

class Author(models.Model):
    full_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING)

class Publisher(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)

class Language(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)

class CoverOption(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)

class Subject(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)

class Series(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    other_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)

class ATOSBookLevel(models.Model):
    name = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)

class ArPoints(models.Model):
    name = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)

class InterestLevel(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)

class ReadingLevel(models.Model):
    name = models.DecimalField(max_digits=3, decimal_places=1)

class LexileLevel(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)

class QuizNumber(models.Model):
    name = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)

class Rating(models.Model):
    name = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)

class Book(models.Model):
    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)
    author = models.ForeignKey('Author', on_delete=models.DO_NOTHING)
    publisher = models.ForeignKey('Publisher', on_delete=models.DO_NOTHING)
    num_of_pages = models.PositiveIntegerField()
    language = models.ForeignKey('Language', on_delete=models.DO_NOTHING)
    cover_option = models.ForeignKey('CoverOption', on_delete=models.DO_NOTHING)
    description = models.TextField()
    memo = models.CharField(max_length=MAX_CHAR_LENGTH_MEMO)
    word_count = models.PositiveIntegerField()
    page_count = models.PositiveIntegerField()
    subject = ListTextField(base_field=models.CharField(max_length=MAX_CHAR_LENGTH), size=20)
    series = ListTextField(base_field=models.CharField(max_length=MAX_CHAR_LENGTH), size=20)
    book_level = models.ForeignKey('ATOSBookLevel', on_delete=models.DO_NOTHING)
    ar_points = models.ForeignKey('ArPoints', on_delete=models.DO_NOTHING)
    # age group 
    interest_level = models.ForeignKey('InterestLevel', on_delete=models.DO_NOTHING)
    lexile_level = models.ForeignKey('LexileLevel', on_delete=models.DO_NOTHING)
    quiz_number = models.ForeignKey('QuizNumber', on_delete=models.DO_NOTHING)
    rating = models.ForeignKey('Rating', on_delete=models.DO_NOTHING)
    reading_level = models.ForeignKey('ReadingLevel', on_delete=models.DO_NOTHING)
    slug = models.SlugField()
    # create_datetime = models.DateTimeField(auto_now_add=True)

class Location(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.TextField()

class Condition(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)

class Status(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)

class Action(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)

class Currency(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    code = models.CharField(max_length=5)

class Inventory(models.Model):
    book = models.ForeignKey('Book', on_delete=models.DO_NOTHING)
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_currency = models.ForeignKey('Currency', on_delete=models.DO_NOTHING)
    acquired_date = models.DateField()
    retired_date = models.DateField()
    location = models.ForeignKey('Location', on_delete=models.DO_NOTHING)
    condition = models.ForeignKey('Condition', on_delete=models.DO_NOTHING)
    status = models.ForeignKey('Status', on_delete=models.DO_NOTHING)
    action = models.ForeignKey('Action', on_delete=models.DO_NOTHING)
    memo = models.CharField(max_length=MAX_CHAR_LENGTH_MEMO)
    # create_datetime = models.DateTimeField(auto_now_add=True)
