from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("users/<int:user_id>", views.view_user),
    path("users/<int:user_id>/add_wallpost", views.post_on_wall),
    path("posts/<int:post_id>/add_comment", views.comment_on_post),
    path("posts/<int:post_id>/delete", views.delete_post),
    path("comments/<int:comment_id>/delete", views.delete_comment),
    path("users/<int:user_id>/friends", views.show_friends),
    path("users/search", views.search_users),
    path("users/search/<str:first_name>/<str:last_name>/<str:username>/<str:email>", views.show_user_search),
    path("users/<int:user_id>/friends/search", views.search_friends),
    path("users/<int:user_id>/add_friend", views.add_friend),
    path("users/<int:user_id>/accept_friend", views.accept_friend),
    path("users/<int:user_id>/ignore_friend", views.ignore_friend),
    path("users/<int:user_id>/remove_friend", views.remove_friend),


    


]