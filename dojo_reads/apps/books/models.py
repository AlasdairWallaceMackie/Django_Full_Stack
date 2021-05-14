from django.db import models
from ..login_and_reg_app.models import *
import re

MAXIMUM_RATING = 5

class Author_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        NAME_REGEX = re.compile(r'^[A-Za-z-.\'\w]+$')

        if len(post_data['first_name']) < 1 or len(post_data['first_name']) > 31 or len(post_data['last_name']) < 1 or len(post_data['last_name']) > 31:
            errors['name_length'] = "First and last name must be between 1 and 31 characters"

        if not re.match(post_data['first_name']) or not re.match(post_data['last_name']):
            errors['name_illegal_characters'] = "Please use valid characters in the name"

class Book_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        title_length = len(post_data['title'])
        if title_length < 1 or title_length > 127:
            errors['title_length'] = "Title must be between 1 and 127 characters"

        if post_data['author_from_list'] == "" and post_data['new_author'] == "":
            errors['no_author'] = "Please add choose an author"
        

class Review_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['text']) < 1:
            errors['text_length'] = "Please write a review"

        if post_data['rating'] < 1 or post_data['rating'] > MAXIMUM_RATING:
            errors['rating_out_of_bounds'] = "Rating must be between 1 and 5"


class Author(models.Model):
    first_name = models.CharField(max_length=31)
    last_name = models.CharField(max_length=31)
    #books - ForeignKey

    objects = Author_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length=127)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    #reviews - ForeignKey

    objects = Book_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    text = models.TextField(null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()

    objects = Review_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def filled_stars(self):
        return range(self.rating)

    def empty_stars(self):
        return range(MAXIMUM_RATING - self.rating)

