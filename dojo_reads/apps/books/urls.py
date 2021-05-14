from django.urls import path
from . import views

urlpatterns = [
    path('', views.books),
    path('new', views.new_book_form),
    path('<int:id>', views.book_detail),
    path('<int:id>/reviews', views.review),
    path('<int:id>/reviews/<int:review_id>', views.modify_review),
]