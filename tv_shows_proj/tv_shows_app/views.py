from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *

def index(request):
    return redirect('/shows')

def template_shows_list(request):
    context = {
        'shows': Show.objects.all()
    }
    return render(request, 'shows_list.html', context)

def template_add_show(request):
    return render(request, 'add_show.html')

def template_show(request, id):
    print("Release date:")
    print( Show.objects.get(id = id).release_date )
    context = {
        'show': Show.objects.get(id = id)
    }
    return render(request, 'show_info.html', context)

def template_edit_show(request, id):
    context = {
        'show': Show.objects.get(id = id)
    }
    return render(request, 'edit_show.html', context)

def db_add_show(request):
    Show.objects.create(
        title = request.POST['title'],
        network = request.POST['network'],
        release_date = request.POST['release_date'],
        description = request.POST['description'],
    )
    return redirect('/')

def db_update_show(request, id):
    show_to_update = Show.objects.get(id = id)
    show_to_update.title = request.POST['title']
    show_to_update.network = request.POST['network']
    show_to_update.release_date = request.POST['release_date']
    show_to_update.description = request.POST['description']
    show_to_update.save()
    return redirect(f'/shows/{show_to_update.id}')

def db_delete_show(request, id):
    show_to_delete = Show.objects.get(id = id)
    show_to_delete.delete()
    return redirect('/')
