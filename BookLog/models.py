from django.db import models

# Create your models here.


class books(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    borrow_count = models.IntegerField(default=0)
    available = models.BooleanField(default=1)

    def __str__(self):
        return str(self.book_id)
    
    class Meta:
        db_table = "books"

class borrowers(models.Model):
    borrower_id = models.AutoField(primary_key=True)
    borrower_name = models.CharField(max_length=30)
    #borrowed_book = models.ForeignKey(books)
    active_book_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return str(self.borrower_name)
    
    class Meta:
        db_table = "borrowers"

class loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    borrower = models.ForeignKey(borrowers, on_delete= models.CASCADE)
    book = models.ForeignKey(books, on_delete= models.CASCADE)
    return_status = models.BooleanField(default=0)

    def __str__(self):
        return str(self.loan_id)
    
    class Meta:
        db_table = "loan"