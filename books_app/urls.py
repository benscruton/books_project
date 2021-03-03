from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("users/<int:user_id>", views.view_user),
    path("users/<int:user_id>/add_wallpost", views.post_on_wall),
    path("posts/<int:post_id>/add_comment", views.comment_on_post),
    path("posts/<int:post_id>/delete", views.delete_post),
    path("comments/<int:comment_id>/delete", views.delete_comment),
    


]