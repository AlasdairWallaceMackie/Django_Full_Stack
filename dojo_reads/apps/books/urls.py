from django.urls import path
from . import views

urlpatterns = [
    path('', views.books),
    path('new', views.new_book_form),
    path('<int:id>', views.book_detail),
]