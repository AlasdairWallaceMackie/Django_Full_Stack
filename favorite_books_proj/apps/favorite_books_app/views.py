from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *

def books(request):
    context = {
        'books': Book.objects.all().order_by('-created_at'),
        'current_user': User.objects.get(id = request.session['current_user_id']),
    }
    return render(request, 'books.html', context)

def create(request):
    if request.method == 'POST':
        errors = Book.objects.basic_validator(request.POST)
        if errors:
            for k,v in errors.get_items():
                messages.error(request, v)
            return redirect('/books')

        current_user = User.objects.get(id = request.session['current_user_id'])
        new_book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by_id = current_user,
        )
        new_book.favorites.add(current_user)

    return redirect('/books')

def show_book(request, id):
    try:
        book = Book.objects.get(id = id)
    except:
        return HttpResponse("<h1>ERROR: Book does not exist</h1>")
    context = {
        'book': book,
        'current_user': User.objects.get(id = request.session['current_user_id']),
        'uploaded_by_user': uploaded_by_current_user(request, book),
        'is_favorite': book.is_favorite(request)
    }
    return render(request, 'show_book.html', context)

def update_book(request, id):
    if request.method == 'POST':
        errors = Book.objects.basic_validator(request.POST)
        if errors:
            print("Errors updating book")
            for k,v in errors.get_items():
                print(v)

        book_to_edit = Book.objects.get(id = id)
        book_to_edit.title = request.POST['title']
        book_to_edit.desc = request.POST['desc']
        book_to_edit.save()

        messages.info(request, "Updated successfully")
        print("Updated successfully")
            
    return redirect(f"/books")

def delete_book(request, id):
    try:
        book_to_delete = Book.objects.get(id=id)
    except:
        return HttpResponse("<h1>Book not found, unable to delete</h1>")
    book_to_delete.delete()
    return redirect('/books')

def is_logged_in(request):
    if request.session.has_key('current_user_id'):
        return True
    else:
        return False

def uploaded_by_current_user(request, book):
    print(f"This book was uploaded by: {book.uploaded_by_id.get_full_name()}")
    if request.session['current_user_id'] == book.uploaded_by_id.id:
        return True
    else:
        return False

def is_favorite(request, book):
    user = User.objects.get(id = request.session['current_user_id'])
    if book.favorites.filter(id = request.session['current_user_id']):
        print("This book is in the current user's favorites")
        return True
    else:
        print("This book is not in the user's favorites")
        return False

def add_favorite(request, id):
    user = User.objects.get(id = request.session['current_user_id'])
    book_to_edit = Book.objects.get(id=id)
    book_to_edit.favorites.add(user)
    return redirect(f"/books/{id}")

def remove_favorite(request, id):
    user = User.objects.get(id = request.session['current_user_id'])
    book_to_edit = Book.objects.get(id=id)
    book_to_edit.favorites.remove(user)
    return redirect(f"/books/{id}")


def show_favorites(request):
    user = User.objects.get(id = request.session['current_user_id'])
    context = {
        'current_user': user,
        'favorites': user.favorites.all()
    }
    return render(request, 'favorites.html', context)