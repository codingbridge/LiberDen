import uuid
from django.db import models
from django_mysql.models import ListTextField

MAX_CHAR_LENGTH = 100
MAX_CHAR_LENGTH_DESCRIPTION = 200
MAX_CHAR_LENGTH_MEMO = 500

class Country(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    other_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

class Author(models.Model):
    full_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING)
    is_deleted = models.BooleanField(default=False)

class Publisher(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)
    is_deleted = models.BooleanField(default=False)

class Language(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

class CoverOption(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

class Subject(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

class Series(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    other_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)
    is_deleted = models.BooleanField(default=False)

class ATOSBookLevel(models.Model):
    name = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

class ArPoints(models.Model):
    name = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

# age group 
class InterestLevel(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

class ReadingLevel(models.Model):
    name = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

class LexileLevel(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

class QuizNumber(models.Model):
    name = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

class Rating(models.Model):
    name = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.CharField(max_length=MAX_CHAR_LENGTH)
    is_deleted = models.BooleanField(default=False)

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=MAX_CHAR_LENGTH_DESCRIPTION)
    author = models.ForeignKey('Author', on_delete=models.DO_NOTHING)
    publisher = models.ForeignKey('Publisher', on_delete=models.DO_NOTHING)
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
    interest_level = models.ForeignKey('InterestLevel', on_delete=models.DO_NOTHING)
    lexile_level = models.ForeignKey('LexileLevel', on_delete=models.DO_NOTHING)
    quiz_number = models.ForeignKey('QuizNumber', on_delete=models.DO_NOTHING)
    rating = models.ForeignKey('Rating', on_delete=models.DO_NOTHING)
    reading_level = models.ForeignKey('ReadingLevel', on_delete=models.DO_NOTHING)
    slug = models.SlugField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_datetime = models.DateTimeField(null=True, blank=True)
