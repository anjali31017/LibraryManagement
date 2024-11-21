# Generated by Django 4.2 on 2024-11-20 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookLog', '0005_rename_book_loan_book_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='book_id',
            new_name='books',
        ),
        migrations.RenameField(
            model_name='loan',
            old_name='borrower_id',
            new_name='borrowers',
        ),
        migrations.AlterField(
            model_name='loan',
            name='return_status',
            field=models.BooleanField(default=0),
        ),
    ]