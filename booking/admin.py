from django.contrib import admin

from .models import Room_type, Room, Booking, Method, Payment

# Register your models here.
admin.site.register(Room_type)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Method)
admin.site.register(Payment)
