from django.shortcuts import render, redirect, HttpResponse
from login_app.models import User
from .models import *

# Create your views here.
def index(request):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request, "dashboard.html", context)

def add_book(request):
    context = {
        'book' : Book.objects.all(),
    }
    return render(request, "add_book.html", context)

def create_book(request):
    book = Book.objects.create(
        title = request.POST['title'],
        author_firstname = request.POST['author_firstname'],
        author_lastname = request.POST['author_lastname'],
        description = request.POST['description'],
        year = request.POST['year'],
        ISBN = request.POST['ISBN'],
    )
    return redirect(f'/books/{book.id}')

def book_detail(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id),
        "user": User.objects.get(id=request.session['user_id']),
        "shelves": Shelf.objects.filter(owner=User.objects.get(id=request.session['user_id'])),
        }
    return render(request, "book_detail.html", context)

def search_book(request, book_id):
    Book.objects.filter(
        title = request.POST['title'],
        author_firstname = request.POST['author_firstname'],
        author_lastname = request.POST['author_lastname'],
        ISBN = request.POST['ISBN']
    )
    return redirect(f"/books/{book_id}")


def view_user(request, user_id):
    context = {
        "user": User.objects.get(id = user_id),
    }
    return render(request, "user_page.html", context)


def post_on_wall(request, user_id):
    WallPost.objects.create(
        contents = request.POST["add_post"],
        poster = User.objects.get(id = request.session["user_id"]),
        wall = User.objects.get(id = user_id)
    )
    return redirect(f"/users/{user_id}")


def comment_on_post(request, post_id):
    this_comment = Comment.objects.create(
        contents = request.POST["comment"],
        commenter = User.objects.get(id = request.session["user_id"]),
        parent = WallPost.objects.get(id = post_id)
    )
    return redirect(f"/users/{this_comment.parent.wall.id}")


def delete_post(request, post_id):
    this_post = WallPost.objects.get(id = post_id)
    redirect_id = this_post.wall.id

    this_post.delete()    

    return redirect(f"/users/{redirect_id}")


def delete_comment(request, comment_id):
    this_comment = Comment.objects.get(id=comment_id)
    # its_parent = WallPost.objects.get(id = this_comment.parent.id)
    redirect_id = WallPost.objects.get(id = this_comment.parent.id).wall.id

    this_comment.delete()



    return redirect(f"/users/{redirect_id}")

def user_shelves(request):
    user = User.objects.get(id=request.session['user_id'])
    shelves = Shelf.objects.filter(owner=User.objects.get(id=request.session['user_id']))
    context = {
        "user": user,
        "shelves": shelves,
    }
    return render(request, "user_shelves.html", context)

def create_shelf(request):
    user = User.objects.get(id=request.session['user_id'])
    shelf = Shelf.objects.create(
        name=request.POST['name'],
        owner = user,
    )
    return redirect(f'user_shelves')

def add_to_shelf(request, book_id):
    shelf_id = request.POST['shelf']
    shelf = Shelf.objects.get(id=shelf_id)
    shelf.books.add(Book.objects.get(id=book_id))

    return redirect(f'/books/{book_id}')

def shelf(request, shelf_id):
    shelf = Shelf.objects.get(id=shelf_id)
    
    context = {
    'shelf': shelf,
    "user": User.objects.get(id=request.session['user_id']),
    "books" : shelf.books.all
    }

    return render(request, "shelf.html", context)
