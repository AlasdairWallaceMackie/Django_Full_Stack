from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index),
    path('users/create', views.create_user),
    path('users/<int:id>', views.show_user),
    path('login', views.login_user),
    path('success', views.success),
    path('logout', views.logout_user),
]