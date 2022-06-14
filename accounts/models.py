from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=9)

    username = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Manager(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=9)
    username = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
