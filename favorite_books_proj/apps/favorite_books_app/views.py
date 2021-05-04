from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *

def books(request):
    context = {
        'books': Book.objects.all(),
        'current_user': User.objects.get(id = request.session['current_user_id']),
    }
    return render(request, 'books.html', context)

def create(request):
    if request.method == 'POST':
        errors = Book.objects.basic_validator(request.POST)
        if errors:
            pass
            return redirect

        current_user = User.objects.get(id = request.session['current_user_id'])
        new_book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by_id = current_user,
        )
        new_book.favorites.add(current_user)

    return redirect('/books')

def show_book(request, id):
    context = {
        'book': Book.objects.get(id = id),
        'current_user': User.objects.get(id = request.session['current_user_id']),
    }
    return render(request, 'show_book.html', context)

def update_book(request, id):
    return HttpResponse(f'Update database with form data., ID: {id}')

def delete_book(request, id):
    return HttpResponse(f'Delete book id: {id} from database')
