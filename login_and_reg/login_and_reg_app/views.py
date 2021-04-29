from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout
import bcrypt

def index(request):
    context = {
        'all_users': User.objects.all()
    }
    if request.session.has_key('current_user_id'):
        request.session['status'] = "logged in"
    return render(request, 'index.html', context)

def create_user(request):
    for k,v in request.POST.items():
        print(f"{k}: {v}")

    errors = User.objects.basic_validator(request.POST)
    if errors:
        print("Errors found in form")
        for k,v in errors.items():
            messages.error(request, v)
        return redirect('/')

    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'].lower(),
        birthday = request.POST['birthday'],
        password = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt() ).decode()
    )

    request.session['current_user_id'] = User.objects.get( email = request.POST['email'].lower() ).id
    request.session['status'] = "registered"
    return redirect('/success')

def login_user(request):
    try:
        user1 = User.objects.get( email = request.POST['login_email'].lower() )
    except:
        messages.error(request, "Email not found")
        return redirect('/')

    if not bcrypt.checkpw( request.POST['login_password'].encode(), user1.password.encode()):
        messages.error(request, "Password is incorrect")
        return redirect('/')
    
    request.session['current_user_id'] = user1.id
    request.session['status'] = "logged in"

    print("************************")
    for k,v in request.session.items():
        print(f"{k}: {v}")

    return redirect('/success')

def logout_user(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if request.session.has_key('current_user_id'):
        context = {
            'current_user': User.objects.get(id = request.session['current_user_id'])
        }
        return render(request, 'success.html', context)
    
    return HttpResponse("""<h1>You are not logged in</h1>
        <a href="/">Return to home page</a>
    """)