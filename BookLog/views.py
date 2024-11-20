import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from BookLog import *
from .models import *
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
