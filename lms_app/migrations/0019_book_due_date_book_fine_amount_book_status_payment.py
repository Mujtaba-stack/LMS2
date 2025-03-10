# Generated by Django 5.1.6 on 2025-03-06 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_app', '0018_rename_member_email_member_member_email_book_member_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='fine_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='book',
            name='status_payment',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=50),
        ),
    ]
