# Generated by Django 4.2 on 2024-11-21 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BookLog', '0008_rename_book_loan_book_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='book_id',
            new_name='book',
        ),
        migrations.RenameField(
            model_name='loan',
            old_name='borrower_id',
            new_name='borrower',
        ),
    ]