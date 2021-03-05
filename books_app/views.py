from django.shortcuts import render, redirect, HttpResponse
from login_app.models import User
from .models import *
from django.contrib import messages

# Create your views here.
def check_friend_requests(data):
    # Call this function from any function that renders a page, if you want friend requests to show up on that page.
    this_user = User.objects.get(id=data["user_id"])
    new_requests = []
    
    if (this_user.added_by.count() > this_user.friends.count()):
        for add in this_user.added_by.all():
            if add not in this_user.friends.all():
                new_requests.append(add)

    return new_requests


def index(request):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "new_requests": check_friend_requests(request.session),
    }
    return render(request, "dashboard.html", context)


# -------- ALL THE BOOK FUNCTIONS --------


def add_book(request):
    context = {
        "new_requests": check_friend_requests(request.session),
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
        "new_requests": check_friend_requests(request.session),
    }
    return render(request, "book_detail.html", context)


def search_book(request):
    title = request.POST["title"]
    first_name = request.POST["author_firstname"]
    last_name = request.POST["author_lastname"]
    isbn = request.POST["ISBN"]   
    
    return redirect(f"/books/search/t={title}/f={first_name}/l={last_name}/i={isbn}")


def show_book_search(request, title, first_name, last_name, isbn):
    terms = {}

    if len(title) > 2:
        terms["title"] = title[2:]
    if len(first_name) > 2:
        terms["first_name"] = first_name[2:]
    if len(last_name) > 2:
        terms["last_name"] = last_name[2:]
    if len(isbn) > 2:
        terms["isbn"] = isbn[2:]

    if terms == {}:
        messages.error(request, "Please enter at least one search term!")
        return redirect("/")

    options = Book.objects.all()

    if "title" in terms:
        title_terms = terms["title"].split()

        for i in range(len(title_terms)):
            options = options.filter(title__icontains = title_terms[i])

    if "first_name" in terms:
        options = options.filter(author_firstname__istartswith = terms["first_name"])

    if "last_name" in terms:
        options = options.filter(author_lastname__istartswith = terms["last_name"])

    if "isbn" in terms:
        options = options.filter(ISBN = terms["isbn"])

    context = {
        "options": options,
        "new_requests": check_friend_requests(request.session),
    }

    return render(request, "list_book_search.html", context)

    

# -------- ALL THE SHELF FUNCTIONS --------

def user_shelves(request, user_id = "none"):
    if user_id == "none":
        user_id = request.session["user_id"]

    context = {
        "user": User.objects.get(id=user_id),
        "editing": False,
        "new_requests": check_friend_requests(request.session),
    }
    return render(request, "user_shelves.html", context)


def edit_shelf(request, shelf_id):
    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "editing": True,
        "edit_shelf_id": shelf_id,
        "new_requests": check_friend_requests(request.session),
    }
    return render(request, "user_shelves.html", context)


def update_shelf(request, shelf_id):
    errors = Shelf.objects.basic_validator(request.POST, request.session["user_id"])

    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f"/shelves/{shelf_id}/edit")

    this_shelf = Shelf.objects.get(id=shelf_id)
    this_shelf.name = request.POST["name"]
    this_shelf.save()

    return redirect("/shelf")


def delete_shelf(request, shelf_id):

    this_shelf = Shelf.objects.get(id=shelf_id)
    this_shelf.delete()
    return redirect("/shelf")


def create_shelf(request):
    errors = Shelf.objects.basic_validator(request.POST, request.session["user_id"])

    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f"/users/{request.session['user_id']}/shelves")


    Shelf.objects.create(
        name=request.POST['name'],
        owner = User.objects.get(id=request.session['user_id']),
    )
    return redirect(f"/users/{request.session['user_id']}/shelves")


def add_to_shelf(request, book_id):
    this_shelf = Shelf.objects.get(id=request.POST['shelf'])
    this_shelf.books.add(Book.objects.get(id=book_id))
    this_shelf.save()
    if this_shelf.name == "Finished":
        print("*"*80)
        print("Finished a book, eh?")

    return redirect(f'/shelves/{this_shelf.id}')


def remove_from_shelf(request, book_id, shelf_id):
    this_book = Book.objects.get(id=book_id)
    this_shelf = Shelf.objects.get(id=shelf_id)
    this_shelf.books.remove(this_book)
    this_shelf.save()

    return redirect(f"/shelves/{shelf_id}")


def shelf(request, shelf_id):
    shelf = Shelf.objects.get(id=shelf_id)
    
    context = {
    'shelf': shelf,
    "user": User.objects.get(id=request.session['user_id']),
    "books" : shelf.books.all,
    "new_requests": check_friend_requests(request.session),
    }

    return render(request, "shelf.html", context)


def recommend_book(request, book_id):
    this_book = Book.objects.get(id=book_id)
    recommender = User.objects.get(id=request.session["user_id"])
    recommendee = User.objects.get(id=request.POST["friend_id"])
    appropriate_shelf = recommendee.shelves.get(name = "Recommended")
    print(f"{recommender.first_name} wants to put {this_book.title} on {recommendee.first_name}'s {appropriate_shelf.name} shelf!")

    appropriate_shelf.books.add(this_book)
    appropriate_shelf.save()

    return redirect(f"/shelves/{appropriate_shelf.id}")




# -------- USER FUNCTIONS: BASIC --------


def view_user(request, user_id):
    this_user = User.objects.get(id=user_id)
    logged_in_user = User.objects.get(id=request.session["user_id"])

    context = {
        "user": this_user,
        "wallposts": WallPost.objects.filter(wall = this_user).order_by("-created_at"),
        "new_requests": check_friend_requests(request.session),
    }

    if user_id == request.session["user_id"]:
        return render(request, "my_profile.html", context)

    context["logged_in_user"] = logged_in_user
    context["mutual_friends"] = User.objects.filter(friends__in=[this_user]).filter(friends__in=[logged_in_user])

    return render(request, "user_page.html", context)


# -------- USER FNS: WALL STUFF --------


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


# -------- USER FNS: FRIENDS AND SEARCHES --------


def show_friends(request, user_id):
    context = {
        "user": User.objects.get(id=user_id),
        "new_requests": check_friend_requests(request.session),
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
        return redirect(f"/users/{request.session['user_id']}/friends")

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
        "options": options,
        "new_requests": check_friend_requests(request.session),
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
            "options": options,
            "new_requests": check_friend_requests(request.session),
        }
    return render(request, "list_friend_search.html", context)
    

def add_friend(request, user_id):
    potential_friend = User.objects.get(id=user_id)
    logged_in_user = User.objects.get(id=request.session["user_id"])

    logged_in_user.added_friends.add(potential_friend)
    logged_in_user.save()

    return redirect(f"/users/{user_id}")



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
