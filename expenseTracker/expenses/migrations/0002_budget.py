# Generated by Django 4.0.2 on 2022-04-06 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.DecimalField(decimal_places=2, default='0', max_digits=8)),
            ],
            options={
                'verbose_name_plural': 'Budget',
            },
        ),
    ]