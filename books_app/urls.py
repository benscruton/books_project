from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("books/add", views.add_book, name="add_book"),
    path("books/search", views.search_book, name="search_book"),
    path("books/create", views.create_book, name="create_book"),
    path("books/<int:book_id>", views.book_detail, name="book_detail"),
    path("users/<int:user_id>", views.view_user),
    path("users/<int:user_id>/add_wallpost", views.post_on_wall),
    path("posts/<int:post_id>/add_comment", views.comment_on_post),
    path("posts/<int:post_id>/delete", views.delete_post),
    path("comments/<int:comment_id>/delete", views.delete_comment),
    path('shelf', views.user_shelves, name="user_shelves"),
    path('shelf/create', views.create_shelf, name="create_shelf"),
    path('book/<int:book_id>/shelf/add', views.add_to_shelf, name="add_to_shelf"),
    path('shelf/<int:shelf_id>', views.shelf, name="shelf_id"),
    path("users/<int:user_id>/friends", views.show_friends),
    path("users/search", views.search_users),
    path("users/search/<str:first_name>/<str:last_name>/<str:username>/<str:email>", views.show_user_search),

    


]