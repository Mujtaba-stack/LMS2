from django.db import models
from django.utils import timezone


# Create your models here.
class DateTimeMixin(models.Model):
    created = models.DateTimeField(default=timezone.now) 
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Category(DateTimeMixin):
    category_name = models.CharField(max_length=220, default="Fiction" , choices=[('Fiction','Fiction'),('Non-Fiction','Non-Fiction'),('Sci-Fic','Sci-Fic')])
    def __str__(self):
        return self.category_name


class Book(DateTimeMixin):
    book_id = models.AutoField(primary_key=True)
    book_title = models.CharField(max_length=220)
    isbn = models.CharField(max_length=20)
    description = models.TextField(default="")
    member = models.ManyToManyField('Member', related_name='borrowed_books', blank=True)
    book_status = models.CharField(max_length=50, choices=[('Available', 'Available'), ('Reserved', 'Reserved'),('Borrowed', 'Borrowed')], default="Available")
    

class Author(DateTimeMixin):
    author_name = models.CharField(max_length=220)

    def __str__(self):
        return self.author_name


class Member(DateTimeMixin):
    member_full_name = models.CharField(max_length=220)
    member_email = models.CharField(max_length=220)
    member_department = models.CharField(max_length=220)
    member_city = models.CharField(max_length=220)
    member_age = models.IntegerField()
    expiry_date = models.DateField()
    books = models.ManyToManyField('Book', related_name='members', blank=True)
    def __str__(self):
        return self.member_full_name










