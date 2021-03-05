from django.db import models
from login_app.models import User

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length = 255)
    year = models.IntegerField()
    description = models.TextField()
    author_firstname = models.CharField(max_length = 255)
    author_lastname = models.CharField(max_length = 255)
    ISBN = models.CharField(max_length = 255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)


class ShelfManager(models.Manager):
    def basic_validator(self, post_data, user_id):
        errors = {}
        this_user = User.objects.get(id=user_id)

        if len(post_data["name"]) < 1:
            errors["name"] = "Your shelf needs to have a name!"
        if len(this_user.shelves.filter(name = post_data["name"])) > 0:
            errors["name"] = "You already have a shelf with this name!"
        
        return errors

class Shelf(models.Model):
    name = models.CharField(max_length = 255)
    books = models.ManyToManyField(Book, related_name = "shelves")
    owner = models.ForeignKey(User, related_name = "shelves", on_delete = models.CASCADE)
    fixed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ShelfManager()


class Parent(models.Model):
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)


class WallPost(Parent):
    poster = models.ForeignKey(User, related_name = "posts", on_delete = models.CASCADE)
    wall = models.ForeignKey(User, related_name = "posts_on_wall", on_delete = models.CASCADE)


class Review(Parent):
    reviewer = models.ForeignKey(User, related_name = "reviews", on_delete = models.CASCADE)
    book = models.ForeignKey(Book, related_name = "reviews", on_delete = models.CASCADE)
    stars = models.IntegerField()


class Comment(models.Model):
    contents = models.TextField()
    commenter = models.ForeignKey(User, related_name = "comments", on_delete = models.CASCADE)
    parent = models.ForeignKey(Parent, related_name = "comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)