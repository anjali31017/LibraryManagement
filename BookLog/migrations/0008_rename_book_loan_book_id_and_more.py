# Generated by Django 4.2 on 2024-11-21 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BookLog', '0007_rename_books_loan_book_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='book',
            new_name='book_id',
        ),
        migrations.RenameField(
            model_name='loan',
            old_name='borrower',
            new_name='borrower_id',
        ),
    ]
