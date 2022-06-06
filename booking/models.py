from django.db import models
from accounts.models import Customer


# Create your models here.


class Room_type(models.Model):
    price = models.FloatField()
    beds = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.beds} beds - ${self.price}"


class Room(models.Model):
    occupancy = models.BooleanField(default=False)
    name = models.CharField(max_length=20)
    room_type = models.ForeignKey(Room_type, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="media/")
    size = models.CharField(max_length=20)
    accesories = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Booking(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.customer.first_name} {self.customer.first_name}"


class Method(models.Model):
    date = models.DateField()
    method = models.CharField(max_length=10)

    def __str__(self):
        return self.method


class Payment(models.Model):
    date = models.DateField()
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)
