from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        errors = {}
        users_with_email = User.objects.filter(email = post_data["email"])

        if len(post_data["first_name"]) < 2:
            errors["first_name"] = "First name must have at least two characters."
        if len(post_data["last_name"]) < 2:
            errors["last_name"] = "Last name must have at least two characters."
        if not EMAIL_REGEX.match(post_data["email"]):
            errors["email"] = "You must use a valid email address to register."
        if len(users_with_email) > 0:
            errors["email"] = "There is already a user registered with this email address."
        if len(post_data["password"]) < 8:
            errors["password"] = "Your password must be at least 8 characters long."
        if not (post_data["password"] == post_data["confirm_pw"]):
            errors["confirm_pw"] = "Passwords did not match."

        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    hashed_pw = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()