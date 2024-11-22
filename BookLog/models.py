from django.db import models

# Create your models here.


class books(models.Model):
    """
    This model is representing books in the library.

    Attributes:
        book_id (int): Autoincrement and primary key.
        book_name (str): The name of the book.
        author (str): The author of the book.
        borrow_count (int): Total times the book is being borrowed.
        available (bool): Availability of book.
    """
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
    """
    This model is representing borrowers of the book.

    Attributes:
        borrower_id (int): Autoincrement and primary key.
        borrower_name (str): The name of the borrower.
        author (str): The author of the book.
        active_book_count (int): Total number of book borrowed.
        is_active (bool): Membership status.
    """
    borrower_id = models.AutoField(primary_key=True)
    borrower_name = models.CharField(max_length=30)
    active_book_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return str(self.borrower_name)
    
    class Meta:
        db_table = "borrowers"

class loan(models.Model):
    """
    This model is representing borrowers of the book.

    Attributes:
        loan_id (int): Autoincrement and primary key.
        borrower (int): ForeignKey to the borrowers table.
        book (int): ForeignKey to the books table.
        is_active (bool): book return status.
    """
    loan_id = models.AutoField(primary_key=True)
    borrower = models.ForeignKey(borrowers, on_delete= models.CASCADE)
    book = models.ForeignKey(books, on_delete= models.CASCADE)
    return_status = models.BooleanField(default=0)

    def __str__(self):
        return str(self.loan_id)
    
    class Meta:
        db_table = "loan"