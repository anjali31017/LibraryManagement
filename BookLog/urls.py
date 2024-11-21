from django.contrib import admin
from django.urls import path, include
from BookLog import *
from .views import *

urlpatterns = [
    path('books/', BookManagementView.as_view(), name='book-create'),
    #path('books/?available=true', BookManagementView.as_view(), name='book-create'),

    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('return/', ReturnBookView.as_view(), name='return-book'),

    path('borrowed/<int:borrower_id>/', ListBorrowedBookView.as_view(), name='list-all-active-book'),
    path('history/<int:borrower_id>/', ListBorrowedBookView.as_view(), name='list-all-borrowed-book'),
]