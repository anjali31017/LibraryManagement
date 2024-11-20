from django.contrib import admin
from django.urls import path, include
from BookLog import *
from .views import *

urlpatterns = [
    path('books/', BookManagementView.as_view(), name='book-create'),
    #path('books/?available=true', BookManagementView.as_view(), name='book-create'),

    path('borrow/', BorrowView.as_view(), name='borrow-book'),

]