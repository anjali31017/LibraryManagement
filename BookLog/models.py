from django.db import models

# Create your models here.


class books(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    available = models.BooleanField(default=1)

    def __str__(self):
        return self.book_name
    
    class Meta:
        db_table = "books"