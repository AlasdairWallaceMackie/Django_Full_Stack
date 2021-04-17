from django.db import models
from django.db.models.fields import CharField, DateField, DateTimeField, TextField

class Show(models.Model):
    title = CharField(max_length=32)
    network = CharField(max_length=32)
    release_date = DateField()
    description = TextField()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def release_date_month_day_year(self):
        return ( self.release_date.strftime("%Y-%m-%d") )
