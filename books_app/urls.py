from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("users/<int:user_id>", views.view_user),
]