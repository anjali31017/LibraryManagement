from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from BookLog import *
from .models import *
from django.db.models import F
# Create your views here.

class BookManagementView(APIView):
    def post(self,request):
        book_name = request.data.get('book_name')
        author = request.data.get('author')
        book_details = {
            "book_name" : book_name,
            "author" : author,
            "available":True
        }
        #optional : add validation & check already exists
        try:
            new_book = books.objects.create(**book_details)
            #new_book_1 = book.objects.create(book_details)
            print(new_book)
            #print(new_book_1)
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
        try:
            available_param = request.query_params.get('available', None)
            #print(available_param)
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

            
            #print(book_available_values)

            #book_data_values = book_data.values()
            # print(book_data)
            #print(book_data_values)
            # data = list(book_data)
            # print(book_data)
            # print(list(book_data))
            return Response({
                "status" : 200,
                "message" : "success",
                "Books" : book_data_values,
                #"books available" : book_available_values
            })
        except Exception as e: 
            return Response({
                'status': 500,
                'error' : e
            })
        

class BorrowView(APIView):
    def post(self,request):
        book_id = request.data.get('book_id')
        borrower_id = request.data.get('borrower_id')

        borrower_status = borrowers.objects.filter(borrower_id=borrower_id)#.values('is_active','active_book_count')
        borrower_details = borrower_status.first()

        #a = borrower.is_active
        #print(a)
        # borrower_status_values = list(borrower_status.values())
        # print(borrower_status_values)
        # a = borrower_status[0]['is_active']
        # print(a)

        # if borrower_details.is_active == False or borrower_details.active_book_count >=3 :
        #     return Response({
        #         'status':400,
        #         'message':'user is inactive or user has already borrowed 3 books',
        #     })
        
        book_available = books.objects.filter(book_id=book_id, available=True)#.values('book_id')
        book_details = book_available.first()
        # book_2 = books.objects.get(book_id = book_id)
        # print(book_available)
        # print(book_1)
        # print(book_2)

        #print(book_available)
        if book_available:
            #print("yes")
            #book_details = books.objects.get(book_id = bo)

            loan_details = {
                'book': book_details,
                'borrower' : borrower_details,
                'return_status' : 'False'
            }
            #print(loan_details)
            loan_book = loan.objects.create(**loan_details)

            print(loan_book)
            loan_book.save()

            borrower_status.update(active_book_count = F('active_book_count') +1)
            book_available.update(available=False,borrow_count = F('borrow_count') +1)
            return Response({
                'status':200,
                'message':'success',
            })
        return Response({
                'status':400,
                'message':'book not available',
            })
            
