from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def index(request):
    return render(request, "dashboard.html")

def add_book(request):
    return render(request, "add_book.html")

def create_book(reaquest, book_id):
    return redirect(f"books/{book_id}")

def book_detail(request):
    return render(request, "book_detail.html")