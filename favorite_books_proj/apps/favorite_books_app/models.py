from django.db import models
from ..login_and_reg_app.models import User


class Book_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['title']) < 1:
            errors['no_title'] = "Title is required"

        if len(post_data['desc']) < 5:
            errors['desc_too_short'] = "Description must be at least 5 characters"

        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books_uploaded")
    favorites = models.ManyToManyField(User, related_name="favorites")

    objects = Book_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_favorite(self, request):
        if self.favorites.filter(id = request.session['current_user_id']):
            return True
        else:
            return False