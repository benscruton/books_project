from django.shortcuts import render, redirect
import bcrypt
from .models import User
from books_app.models import Shelf
from django.contrib import messages

# Create your views here.

def login_index(request):
    # if "user_id" in request.session:
    #     return redirect("/")

    return render(request, "login_index.html")


def register_new_user(request):
    errors = User.objects.basic_validator(request.POST)

    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect("/login")

    this_user = User.objects.create(
        first_name = request.POST["first_name"],
        last_name = request.POST["last_name"],
        email = request.POST["email"],
        username = request.POST["username"],
        hashed_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        )

    if this_user.username == "":
        this_user.username = this_user.email
        this_user.save()

    Shelf.objects.create(
        name = "Reading",
        owner = this_user,
        fixed = True
    )

    Shelf.objects.create(
        name = "Finished",
        owner = this_user,
        fixed = True
    )

    Shelf.objects.create(
        name = "To Read",
        owner = this_user,
        fixed = True
    )

    Shelf.objects.create(
        name = "Recommended",
        owner = this_user,
        fixed = True
    )

    messages.success(request, "Successfully created account!  Please log in:")

    return redirect("/login")


def login(request):
    if len(User.objects.filter(email = request.POST["username"])) == 1:
        this_user = User.objects.get(email = request.POST["username"])
    elif len(User.objects.filter(username = request.POST["username"])) == 1:
        this_user = User.objects.get(username = request.POST["username"])
    else:
        messages.error(request, "User not found!")
        return redirect("/login")

    match = bcrypt.checkpw(request.POST["password"].encode(), this_user.hashed_pw.encode())
    
    if not match:
        messages.error(request, "User and password didn't match.")
        return redirect("/login")

    request.session["user_id"] = this_user.id
    request.session["first_name"] = this_user.first_name
    request.session["last_name"] = this_user.last_name
    request.session["email"] = this_user.email
    
    return redirect(f"/users/{request.session['user_id']}")


def logout(request):
    if "user_id" not in request.session:
        messages.error(request, "You are not logged in!")
        return redirect("/login")

    del request.session["user_id"]
    del request.session["first_name"]
    del request.session["last_name"]
    del request.session["email"]
    return redirect("/login")

# For demonstrational purposes: click a single button to log in as either of two already-created users
def demo_login(request, demo_id):
    if(demo_id == 1):
        this_user = User.objects.get(email = "pol.treidum@death.star")
        request.session["user_id"] = this_user.id
        request.session["first_name"] = this_user.first_name
        request.session["last_name"] = this_user.last_name
        request.session["email"] = this_user.email
    elif(demo_id == 2):
        this_user = User.objects.get(email = "osleo.prennert@yavin.iv")
        request.session["user_id"] = this_user.id
        request.session["first_name"] = this_user.first_name
        request.session["last_name"] = this_user.last_name
        request.session["email"] = this_user.email
    else:
        return redirect("/login")
    return redirect(f"/users/{request.session['user_id']}")