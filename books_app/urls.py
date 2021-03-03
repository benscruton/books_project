from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("books/add", views.add_book, name="add_book"),
    path("books/locate", views.locate_book, name="locate_book"),
    path("books/create", views.create_book, name="create_book"),
    path("books/<int:book_id>", views.book_detail, name="book_detail"),
    path("users/<int:user_id>", views.view_user),
    path("users/<int:user_id>/add_wallpost", views.post_on_wall),
    path("posts/<int:post_id>/add_comment", views.comment_on_post),
    path("posts/<int:post_id>/delete", views.delete_post),
    path("comments/<int:comment_id>/delete", views.delete_comment),
    


]