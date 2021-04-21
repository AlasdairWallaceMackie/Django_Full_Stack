import re
from django.db import models

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