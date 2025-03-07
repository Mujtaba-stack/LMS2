from django.db import models
from django.utils import timezone
from datetime import date



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
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0000)  
    description = models.TextField(default="")
    member = models.ManyToManyField('Member', related_name='borrowed_books', blank=True)
    book_status = models.CharField(max_length=50, choices=[('Available', 'Available'), ('Reserved', 'Reserved'), ('Borrowed', 'Borrowed')], default="Available")


class Billing(DateTimeMixin):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    status_payment = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)  
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  

    def __str__(self):
        return f"Billing for {self.member.member_full_name} - {self.book.book_title}"
    
    def fine_calculation(self):
        if self.return_date and self.due_date: 
            overdue_days = (self.return_date - self.due_date).days  
            if overdue_days > 0:
                self.fine_amount = overdue_days * 4
                self.status_payment = "Pending"
            else:
                self.fine_amount = 0
                self.status_payment = "Paid"
            self.save()

    def payment_process(self):
        self.status_payment = "Paid"  
        self.return_date = timezone.now().date()  
        self.save()






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












