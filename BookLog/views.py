from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from BookLog import *
from .models import *
from django.db.models import F
# Create your views here.

class BookManagementView(APIView):
    def post(self,request):
        """
        POST/books/ (add new book)

        It retrives the book name and author name, checks if data already exists.
        If no, then creates a new entry in the database marking  available = True (book is available)

        Return:
        201: Book added successfully in database
        409: Book already exists

        Exception:
        500: Exception
        """
        try:
            book_name = request.data.get('book_name')
            author = request.data.get('author')
            book_exists = books.objects.filter(book_name=book_name, author = author)
            if book_exists:
                return Response({
                    'status': 409,
                    'message' : 'Book already exists'
                })
            
            book_details = {
                "book_name" : book_name,
                "author" : author,
                "available":True
            }
            new_book = books.objects.create(**book_details)
            new_book.save()
            return Response({
                'status': 201,
                'message' : 'New Book added succcessfully'
            })
        except Exception as e: 
            return Response({
                'status': 500,
                'error' : e
            })
    
    def get(self,request):
        """
        GET/books/ ==> It retrives all book details.
        
        GET/books/?availabe=True ==> It retrives all books which are avaialable.

        GET/books/?availabe=False ==> It retrives all books which are currently loaned out.
        
        Return:
        200 : books available (with and without filter)

        Exception:
        500: Exception
        """
        try:
            available_param = request.query_params.get('available', None)
            book_data = books.objects.all()

            if available_param is not None:
                book_available = book_data.filter(available=available_param)
                book_available_values = list(book_available.values())
                return Response({
                    "status" : 200,
                    "message" : "success",
                    "Books" : book_available_values
            })

            book_data_values = list(book_data.values())
            return Response({
                "status" : 200,
                "message" : "success",
                "Books" : book_data_values,
            })
        except Exception as e: 
            return Response({
                'status': 500,
                'error' : e
            })
        
class BorrowView(APIView):
    def post(self,request):
        """
        POST/borrow/ (borrow a book)

        It borrows a book using borrower_id and book_id.
        Checks if borrower_id is available, is_active = True and total active_book_count is >= 3
        if book is available, it is loaned 
            - marking available status of book in books table as 'False'
            - the active_book_count is incremented by 1 in borrowers table
            - the borrow_count is incremented by 1 in books table

        Return:
        404: user not found (borrower doesnot exists)
        404: book not found (book doesnot exists)
        401: user not found (borrower membership status is not active i.e is_active = False)
        403: User has already borrowed 3 books
        200: Book loaned
        400: Book not available

        Exception:
        500: Exception
        """
        try:
            book_id = request.data.get('book_id')
            borrower_id = request.data.get('borrower_id')

            borrower_status = borrowers.objects.filter(borrower_id=borrower_id)#.values('is_active','active_book_count')
            borrower_details = borrower_status.first()
            book_available = books.objects.filter(book_id=book_id)#.values('book_id')
            book_details = book_available.first()
            
            if not borrower_status: 
                return Response({
                    'status':404,
                    'message':'user not found',
                })  
            if not book_available:
                return Response({
                    'status':404,
                    'message':'Book not found',
                }) 
            if borrower_details.is_active == False : 
                return Response({
                    'status':401,
                    'message':'User is inactive',
                })
            if borrower_details.active_book_count >=3: 
                return Response({
                    'status':403,
                    'message':'User has already borrowed 3 books',
                })
            
            if book_details.available == True:
                loan_details = {
                    'book': book_details,
                    'borrower' : borrower_details,
                    'return_status' : 'False'
                }
                loan_book = loan.objects.create(**loan_details)
                loan_book.save()

                borrower_status.update(active_book_count = F('active_book_count') +1)
                book_available.update(available=False, borrow_count = F('borrow_count') +1)

                return Response({
                    'status':200,
                    'message':'Book borrowed successfully',
                })
            return Response({
                    'status':400,
                    'message':'Book not available (borrowed)',
                })
        except Exception as e:
            return Response({
                    'status':500,
                    'error':e,
                })
            
