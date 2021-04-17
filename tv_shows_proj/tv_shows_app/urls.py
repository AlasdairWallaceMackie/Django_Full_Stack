from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('shows', views.template_shows_list),
    path('shows/new', views.template_add_show),
    path('shows/create', views.db_add_show),
    path('shows/<int:id>', views.template_show),
    path('shows/<int:id>/edit', views.template_edit_show),
    path('shows/<int:id>/update', views.db_update_show),
    path('shows/<int:id>/destroy', views.db_delete_show),
]