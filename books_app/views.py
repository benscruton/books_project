from django.shortcuts import render, redirect, HttpResponse
from login_app.models import User
from .models import *

# Create your views here.
def index(request):
    return HttpResponse("Website works!")


def view_user(request, user_id):
    context = {
        "user": User.objects.get(id = user_id),
    }
    return render(request, "user_page.html", context)