from django.db import models
from django.db.models.fields import CharField, DateField, DateTimeField, TextField
from datetime import datetime


charfield_max_length = 32

class Show_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        #title length 2-32
        if len(post_data['title']) < 2 or len(post_data['title']) > charfield_max_length:
            errors['title_length'] = f"Title must be between 2 and {charfield_max_length} characters"

        #title should be Unique, but it's ok if editing same show
        if 'id' in post_data:
            if Show.objects.get(id = post_data['id']).title != post_data['title']:
                if Show.objects.filter(title = post_data['title']).count() > 0:
                    errors['duplicate_title'] = "Title is already in use"

        #network length 3-32
        if len(post_data['network']) < 3 or len(post_data['title']) > charfield_max_length:
            errors['network_length'] = f"Network name must be between 3 and {charfield_max_length} characters"

        #release date entered and should be in the past
        if post_data['release_date'] == '':
            errors['release_date_not_present'] = "Please enter a date"
        else:
            date_object = datetime.strptime(post_data['release_date'], '%Y-%m-%d')
            if date_object > datetime.now():
                errors['release_date'] = "Release date cannot be in the future"

        #description optional, but if present >=10 characters
        if len(post_data['description']) > 0 and len(post_data['description']) < 10:
            errors['description_length'] = "If you are adding a description, it must be greater than 10 characters"

        print("Errors: ")
        print(errors)
        return errors


class Show(models.Model):
    title = CharField(max_length=charfield_max_length)
    network = CharField(max_length=charfield_max_length)
    release_date = DateField()
    description = TextField()
    objects = Show_Manager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def release_date_month_day_year(self):
        return ( self.release_date.strftime("%Y-%m-%d") )

