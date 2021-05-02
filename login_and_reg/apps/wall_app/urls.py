from django.urls import path
from . import views

urlpatterns = [
    path('wall', views.wall),
    path('wall/message', views.create_message),
    path('wall/message/all', views.all_messages),
    path('wall/message/recent', views.recent_message),
    path('wall/message/<int:id>/destroy', views.delete_message),
    path('wall/comment', views.create_comment),
    path('wall/comment/recent', views.recent_comment),
]