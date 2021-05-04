from django.urls import path
from . import views

urlpatterns = [
    path('', views.books),
    path('create', views.create),
    path('<int:id>', views.show_book),
    path('<int:id>/update', views.update_book),
    path('<int:id>/destroy', views.delete_book),
]