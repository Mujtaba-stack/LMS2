# Generated by Django 5.1.6 on 2025-03-04 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms_app', '0016_delete_borrow_rename_borrowed_books_member_books_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='membership_type',
        ),
    ]
