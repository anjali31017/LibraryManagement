# LibraryManagement

## Overview

This is an API in Django Rest Framework that manages a library system for adding new and listing all books.Also includes borrowing and returning of books. It provides APIs for book management, borrowing, and returning books, as well as tracking borrowed books and borrower history.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)

## Requirements

- Python 3.x
- Django 4.x or higher
- Django REST Framework 3.x or higher
- MySQL

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anjali31017/LibraryManagement.git
   
2. **Create a virtual environment:**
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`

3. **Install dependencies:**
    pip install -r requirements.txt

4. **Set up the database:**
    Update the database settings in settings.py.
    Run migrations:
        python manage.py migrate

5. **Run the development server:**  
    python manage.py runserver

## API Endpoints

1. BookManagementView

    POST /books/: Add a new book.
        URL: http://127.0.0.1:8000/books/
        Request Body: { "book_name": "Book Name", "author": "Author Name"}

    GET /books/: List all books, optionally filtering by availability.
        URL: http://127.0.0.1:8000/books/
             http://127.0.0.1:8000/books/?available=True
             http://127.0.0.1:8000/books/?available=False
        Query Parameters: ?available=true

2. BorrowBookView

    POST /borrow/: Borrow a book using book_id and borrower_id.
        URL: http://127.0.0.1:8000/borrow/
        Request Body: { "book_id": 1, "borrower_id": 1 }
    
3. ReturnBookView

    POST /return/: Return a book by book_id.
        URL: http://127.0.0.1:8000/return/
        Request Body: { "book_id": 1 }

4. ListBorrowedBookView (List Borrowed Books and Borrower History)

    GET /borrowed/<borrower_id>/: List of all active (unreturned) books for a borrower.
    URL: http://127.0.0.1:8000/borrowed/<int:borrower_id>/ 
         (eg:http://127.0.0.1:8000/borrowed/1/)

    GET /history/<borrower_id>/: List of all books ever borrowed by the borrower, including return status.
    URL: http://127.0.0.1:8000/history/<int:borrower_id>/ 
         (eg:http://127.0.0.1:8000/history/1/)


