from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *

def index(request):
    context = {
        'courses': Course.objects.all(),
    }
    return render(request, 'index.html', context)

def create_course(request):
    if request.method =='POST':
        errors = Course.objects.basic_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        new_course = Course.objects.create(
            name = request.POST['name'],
        )
        new_desc = Description(course = new_course, text = request.POST['description'])
        new_desc.save()
    return redirect('/')

def show_course(request, id):
    context = {
        'course': Course.objects.get(id = id)
    }
    return render(request, 'course_page.html', context)

def delete_course(request, id):
    course_to_delete = Course.objects.get(id = id)
    course_to_delete.delete()
    return redirect('/')

def create_comment(request, id):
    errors = Comment.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        Comment.objects.create(
            text = request.POST['comment'],
            course = Course.objects.get(id=id)
        )
    return redirect(f'/courses/{id}/')

def delete_comment(request, id, comment_id):
    comment_to_delete = Comment.objects.get(id=comment_id)
    comment_to_delete.delete()
    
    return redirect(f'/courses/{id}/')
