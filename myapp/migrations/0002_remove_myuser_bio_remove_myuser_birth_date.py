# Generated by Django 5.1.6 on 2025-02-18 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomerce', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='birth_date',
        ),
    ]
