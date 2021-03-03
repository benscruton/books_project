from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("books/add", views.add_book, name="add_book"),
    path("books/locate", views.locate_book, name="locate_book"),
    path("books/create", views.create_book, name="create_book"),
    path("books/<int:book_id>", views.book_detail, name="book_detai")
]