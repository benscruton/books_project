from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),

    path("books/add", views.add_book, name="add_book"),

    path("books/search", views.search_book, name="search_book"),

    path("books/search/<str:title>/<str:first_name>/<str:last_name>/<str:isbn>", views.show_book_search),
    
    path("books/create", views.create_book, name="create_book"),
    
    path("books/<int:book_id>", views.book_detail, name="book_detail"),
    
    path("users/<int:user_id>", views.view_user),
    
    path("users/<int:user_id>/add_wallpost", views.post_on_wall),
    
    path("users/search", views.search_users),
    
    path("users/search/<str:first_name>/<str:last_name>/<str:username>/<str:email>", views.show_user_search),

    path("users/<int:user_id>/friends", views.show_friends),
    
    path("users/<int:user_id>/friends/search", views.search_friends),
    
    path("users/<int:user_id>/add_friend", views.add_friend),
    
    path("users/<int:user_id>/accept_friend", views.accept_friend),
    
    path("users/<int:user_id>/ignore_friend", views.ignore_friend),
    
    path("users/<int:user_id>/remove_friend", views.remove_friend),

    path("posts/<int:post_id>/add_comment", views.comment_on_post),
    
    path("posts/<int:post_id>/delete", views.delete_post),
    
    path("comments/<int:comment_id>/delete", views.delete_comment),

    path("users/<int:user_id>/shelves", views.user_shelves),
    
    path('shelf', views.user_shelves, name="user_shelves"),

    path("shelves", views.user_shelves),
    
    path('shelf/create', views.create_shelf, name="create_shelf"),
    path("shelves/create", views.create_shelf),
    
    path('book/<int:book_id>/shelf/add', views.add_to_shelf, name="add_to_shelf"),
    
    path('shelf/<int:shelf_id>', views.shelf, name="shelf_id"),

    path("shelves/<int:shelf_id>", views.shelf),

    path("shelves/<int:shelf_id>/delete", views.delete_shelf),

    path("shelves/<int:shelf_id>/edit", views.edit_shelf),

    path("shelves/<int:shelf_id>/update", views.update_shelf),



]