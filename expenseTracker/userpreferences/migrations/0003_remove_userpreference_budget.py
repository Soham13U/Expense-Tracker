# Generated by Django 4.0.2 on 2022-04-06 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0002_userpreference_budget'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreference',
            name='budget',
        ),
    ]
