# Generated by Django 4.0.1 on 2022-02-12 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register_user',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='register_user',
            name='year',
        ),
    ]
