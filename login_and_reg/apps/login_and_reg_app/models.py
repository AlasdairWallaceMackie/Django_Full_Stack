from django.db import models
from datetime import date, datetime
import re

class User_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        NAME_REGEX = re.compile( r'^[A-Za-z\'\s]{2,32}$' )
        if not NAME_REGEX.match(post_data['first_name']) or not NAME_REGEX.match(post_data['last_name']):
            errors['invalid_name'] = "First and last name should be between 2 and 32 characters, with valid symbols"

        EMAIL_REGEX = re.compile( r'^[A-Za-z0-9.+_-]+@[A-Za-z0-9+_-]+\.[A-Za-z0-9.]+$' )
        if len(post_data['email']) > 64:
            errors['email_length'] = "Email is too long "

        if not EMAIL_REGEX.match(post_data['email']):
            errors['invalid_email'] = "Please enter a valid email address"

        for user in User.objects.all():
            if user.email == post_data['email'].lower():
                errors['duplicate_email'] = "Email is already in use"

        if post_data['birthday'] != "":
            minimum_days_age = 13 * 365.2425
            if ( datetime.today() - datetime.strptime(post_data['birthday'], '%Y-%m-%d') ).days < minimum_days_age:
                errors['age'] = "You must be at least 13 years old to register an account"
        else:
            errors['birthday_blank'] = "Please enter a date of birth"

        if len(post_data['password']) < 8:
            errors['short_password'] = "Password must be at least 8 characters"

        if post_data['password'] != post_data['confirm']:
            errors['no_match'] = "Password confirmation must match"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    password = models.TextField()
    birthday = models.DateField()
    ##Foreign Keys
        # messages
        # comments
    objects = User_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    user_id = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    message = models.TextField()
    ##Foreign Keys
        # comments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def post_date(self):
        return self.created_at.strftime('%B %d, %Y -- %I:%M %p')

    def author_full_name(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"

class Comment(models.Model):
    user_id = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message_id = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    comment = models.TextField()
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def post_date(self):
        return self.created_at.strftime('%B %d, %Y -- %I:%M %p')

    def author_full_name(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"