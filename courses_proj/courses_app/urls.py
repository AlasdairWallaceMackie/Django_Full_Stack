from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('courses/create/', views.create_course),
    path('courses/<int:id>/', views.show_course),
    path('courses/<int:id>/destroy/', views.delete_course),
    path('courses/<int:id>/create_comment/', views.create_comment),
    path('courses/<int:id>/comments/<int:comment_id>/destroy/', views.delete_comment),
]