# Generated by Django 2.2 on 2021-05-04 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_reg_app', '0004_auto_20210501_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
