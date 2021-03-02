from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_index),
    path("users/register", views.register_new_user),
    path("users/login", views.login),
    path("users/logout", views.logout),
]