from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index),
    path('user', views.create_user),
    path('login', views.login_user),
    path('success', views.success),
    path('logout', views.logout_user),
]