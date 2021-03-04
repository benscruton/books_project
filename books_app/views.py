from django.shortcuts import render, redirect, HttpResponse
from login_app.models import User
from .models import *
from django.contrib import messages

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


def check_friend_requests(data):
    # Call this function from any function that renders a page, if you want friend requests to show up on that page.
    this_user = User.objects.get(id=data["user_id"])
    new_requests = []
    
    if (this_user.added_by.count() > this_user.friends.count()):
        for add in this_user.added_by.all():
            if add not in this_user.friends.all():
                new_requests.append(add)

    return new_requests



def view_user(request, user_id):
    new_requests = check_friend_requests(request.session)

    this_user = User.objects.get(id=user_id)
    logged_in_user = User.objects.get(id=request.session["user_id"])

    context = {
        "user": this_user,
        "wallposts": WallPost.objects.filter(wall = this_user).order_by("-created_at"),
        "new_requests": new_requests
    }

    if user_id == request.session["user_id"]:
        return render(request, "my_profile.html", context)

    context["logged_in_user"] = logged_in_user
    context["mutual_friends"] = User.objects.filter(friends__in=[this_user]).filter(friends__in=[logged_in_user])

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


def show_friends(request, user_id):
    new_requests = check_friend_requests(request.session)

    context = {
        "user": User.objects.get(id=user_id),
        "new_requests": new_requests
    }

    return render(request, "friends.html", context)


def search_users(request):

    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    username = request.POST["username"]
    email = request.POST["email"]
    
    return redirect(f"/users/search/f={first_name}/l={last_name}/u={username}/e={email}")


def show_user_search(request, first_name, last_name, username, email):
    terms = {}

    if len(first_name) > 2:
        terms["first_name"] = first_name[2:]
    if len(last_name) > 2:
        terms["last_name"] = last_name[2:]
    if len(username) > 2:
        terms["username"] = username[2:]
    if len(email) > 2:
        terms["email"] = email[2:]

    if terms == {}:
        messages.error(request, "Please enter at least one search term!")
        return render(request, "list_friend_search.html")

    options = User.objects.all()

    if "first_name" in terms:
        options = options.filter(first_name__istartswith = terms["first_name"])
    if "last_name" in terms:
        options = options.filter(last_name__istartswith = terms["last_name"])
    if "username" in terms:
        options = options.filter(username = terms["username"])
    if "email" in terms:
        options = options.filter(email = terms["email"])

    context = {
        "options": options
    }

    return render(request, "list_friend_search.html", context)



def search_friends(request, user_id):
    terms = request.POST["friend_search"].split()

    if len(terms) <= 0:
        messages.error(request, "Please enter at least one character to search!")
        return redirect(f"/users/{request.session['user_id']}/friends")
    
    all_options = User.objects.get(id=user_id).friends.all()
    options = User.objects.get(id=user_id).friends.all()

    for i in range(len(terms)):
        f_options = all_options.filter(first_name__istartswith = terms[i])
        l_options = all_options.filter(last_name__istartswith = terms[i])
        comb_options = f_options.union(l_options)
        options = options.intersection(comb_options)

        context = {
            "options": options
        }
    return render(request, "list_friend_search.html", context)
    

def add_friend(request, user_id):
    potential_friend = User.objects.get(id=user_id)
    logged_in_user = User.objects.get(id=request.session["user_id"])

    logged_in_user.added_friends.add(potential_friend)
    logged_in_user.save()

    return redirect(f"/users/{user_id}")


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

def accept_friend(request, user_id):
    potential_friend = User.objects.get(id=user_id)
    logged_in_user = User.objects.get(id=request.session["user_id"])

    logged_in_user.added_friends.add(potential_friend)
    logged_in_user.friends.add(potential_friend)
    potential_friend.friends.add(logged_in_user)
    logged_in_user.save()
    potential_friend.save()
    
    return redirect(f"/users/{user_id}")


def ignore_friend(request, user_id):
    potential_friend = User.objects.get(id=user_id)
    logged_in_user = User.objects.get(id=request.session["user_id"])

    potential_friend.added_friends.remove(logged_in_user)
    logged_in_user.save()

    return redirect(f"/users/{user_id}")


def remove_friend(request, user_id):
    enemy = User.objects.get(id=user_id)
    logged_in_user = User.objects.get(id=request.session["user_id"])

    enemy.friends.remove(logged_in_user)
    logged_in_user.friends.remove(enemy)
    logged_in_user.added_friends.remove(enemy)
    logged_in_user.added_by.remove(enemy)
    logged_in_user.save()
    enemy.save()

    return redirect(f"/users/{user_id}")
    
