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


class Payment(models.Model):
    date = models.DateField()
    amount = models.IntegerField()
    cc_number = models.CharField(max_length=16, default="4024007161507339")
    cc_expiry = models.CharField(max_length=5, default="04/12")
    cc_code = models.CharField(max_length=3, default="033")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)
