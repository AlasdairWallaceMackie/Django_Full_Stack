from django.db import models

class Course_Manager(models.Manager):
    def basic_validator(self, post_data):
        pass

class Description_Manager(models.Model):
    def basic_validator(self, post_data):
        pass



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