# Generated by Django 4.0.4 on 2022-06-06 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_manager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
