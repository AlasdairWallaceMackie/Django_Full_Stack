from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def books(request):
    if request.method == "GET":
        context = {
            'current_user': User.objects.get(id = request.session['current_user_id']),
            'reviews': Review.objects.order_by("-created_at"),
            'books': Book.objects.all(),
        }
        return render(request, 'book_reviews.html', context)
    elif request.method == "POST":
        print("POST received to create new book")
        errors = Book.objects.basic_validator(request.POST)
        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('new')

        # Check if new_author is filled out, otherwise take from list
        if request.POST['new_author'] == "":
            author = Author.objects.get( id = request.POST['author_from_list'] )
        else:
            name_split = request.POST['new_author'].split(" ", 1)
            duplicate = Author.objects.filter(first_name = name_split[0], last_name = name_split[1]).first()
            if duplicate:
                author = duplicate
            else:
                author = Author.objects.create(
                    first_name = name_split[0],
                    last_name = name_split[1]
                )
        
        new_book = Book.objects.create(
            title = request.POST['title'],
            author = author
        )
        new_review = Review.objects.create(
            text = request.POST['review'],
            book = new_book,
            reviewer = User.objects.get(id = request.session['current_user_id']),
            rating = request.POST['rating'],
        )
        return redirect(f'/books/{new_book.id}')

def new_book_form(request):
    return render(request, 'add_book.html')

def book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
    except:
        return HttpResponse("<h1>Book not found</h1>")
    context = {
        'book': book
    }
    return render(request, 'book_detail.html', context)

#When deleting reviews, make sure the logged in user actually owns the review
