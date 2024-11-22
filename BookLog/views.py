from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from BookLog import *
from .models import *
from django.db.models import F
# Create your views here.

class BookManagementView(APIView): 
    def post(self,request): # insert multiple books
        """
        POST/books/ (add a new book)

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
                'error' : str(e)
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
            if available_param is not None:
                book_data = books.objects.filter(available=available_param)
            else:
                book_data = books.objects.all()

            book_data_values = list(book_data.values())
            return Response({
                "status" : 200,
                "message" : "success",
                "Books" : book_data_values
            })
        except Exception as e: 
            return Response({
                'status': 500,
                'error' : str(e)
            })
        
class BorrowBookView(APIView):
    def post(self,request):
        try:
            book_id = request.data.get('book_id')
            borrower_id = request.data.get('borrower_id')

            borrower_status = borrowers.objects.filter(borrower_id=borrower_id)
            book_available = books.objects.filter(book_id=book_id)

            borrower_details = borrower_status.first()
            book_details = book_available.first()

            validation_checks = [
                (borrower_details is None, 404, 'User  not found'),
                (book_details is None, 404, 'Book not found'),
            ]

            if borrower_status and book_available:
                validation_checks_extend = [
                (borrower_details.is_active == False, 401, 'User  is inactive'),
                (borrower_details.active_book_count >= 3, 403, 'User  has already borrowed 3 books'),
                (book_details.available == False, 400, 'Book not available (borrowed)')
                ]
                validation_checks.extend(validation_checks_extend)
            
            
            for condition, status, message in validation_checks:
                if condition:
                    return Response({
                        'status': status,
                        'message': message,
                    })
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
        except Exception as e:
            return Response({
                    'status':500,
                    'error':str(e)
                })
            
class ReturnBookView(APIView):
    def post(self,request):
        """
        POST/return/ (return a book)

        It returns a book using book_id.
        Checks if book_id is availableand return_status = False in loan table
        if found,
            - updating return_status = True in loan table
            - updating availability of book in books table as True (available = True)
            - the active_book_count is decremented by 1 in borrowers table

        Return:
        200: Book returned successfully
        400: Book already returned

        Exception:
        500: Exception
        """
        try:
            book_id = request.data.get('book_id')
            loan_details = loan.objects.filter(book = book_id, return_status = False)
            if loan_details:
                loan_details_value = loan_details.first()
                loan_details.update(return_status = True)
                books.objects.filter(book_id = book_id).update(available = True)
                borrowers.objects.filter(borrower_id = loan_details_value.borrower_id).update(active_book_count = F('active_book_count') - 1)
                return Response({
                    'status':200,
                    'message':'Book returned successfully',
                })
            return Response({
                'status':409,
                'message':'Book already returned'
            })
        except Exception as e:
            return Response({
                    'status':500,
                    'error':str(e)
                })
        
class ListBorrowedBookView(APIView):
    def get(self,request, borrower_id):
        """
        Get/borrowed/<int:borrower_id>/ (List all active books of borrower)
        Get/history/<int:borrower_id>/ (List all borrowed books of borrower)

        It returns borrowed book details using borrower_id.

        Return:
        200: Active Books / All Books

        Exception:
        500: Exception
        """
        try:
            action = request.resolver_match.url_name
            msg = "All Books"
            loan_details = loan.objects.select_related('book')
            loan_details = loan_details.filter(borrower = borrower_id)
            
            if action == 'list-all-active-book':
                msg = "Active Books"
                loan_details = loan_details.filter(return_status = False)
            data = [
                    {
                        "loan_id": details.loan_id,
                        "Book": {
                            "book": details.book.book_id,
                            "name": details.book.book_name,
                            "author": details.book.author
                        },
                        "return_status": details.return_status,
                    }
                for details in loan_details
            ]
            return Response({
                    'status':200,
                    'message':msg,
                    'borrowed book count': len(loan_details),
                    'books': data
                })
        except Exception as e:
            return Response({
                    'status':500,
                    'error':str(e)
                })
        

        