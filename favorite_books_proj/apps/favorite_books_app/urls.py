from django.urls import path
from . import views

urlpatterns = [
    path('', views.books),
    path('create', views.create),
    path('<int:id>', views.show_book),
    path('favorites', views.show_favorites),
    path('<int:id>/update', views.update_book),
    path('<int:id>/destroy', views.delete_book),
    path('<int:id>/favorites/add', views.add_favorite),
    path('<int:id>/favorites/remove', views.remove_favorite),
]