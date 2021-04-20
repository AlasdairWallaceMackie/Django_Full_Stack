from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('courses/create', views.create_course),
    path('courses/<int:id>', views.course_template),
    path('courses/<int:id>/destroy', views.delete_course),
]