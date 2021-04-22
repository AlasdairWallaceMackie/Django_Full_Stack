import re
from django.db import models
from django.db.models.fields import DateTimeField

class Course_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['name']) < 5 or len(post_data['name']) > 32:
            errors['name_length'] = "Course name must be between 5 and 32 characters"

        if not post_data['name'].isalpha():
            errors['alphabetic'] = "Course name can only contain alphabetic characters"

        return errors

class Description_Manager(models.Model):
    def basic_validator(self, post_data):
        errors = {}
        
        if len(post_data['description']) < 15:
            errors['description_length'] = "Description must be at least 15 characters long"

        return errors
    
class Comment_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['comment']) < 1:
            errors['empty_comment'] = "Please enter a comment first"
        
        if len(post_data['comment']) > 128:
            errors['comment_too_long'] = "Comment is too long"
        
        return errors


class Course(models.Model):
    name = models.CharField(max_length=32)

    objects = Course_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Description(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField()
    
    objects = Description_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class Comment(models.Model):
    text = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comments")

    objects = Comment_Manager()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)