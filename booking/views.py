from django.shortcuts import render, redirect
from datetime import date
from .models import Room, Booking, Payment, Room_type
from accounts.models import Customer, Manager
from .forms import AddRoom, EditCustomer, FilterForm, BookingForm2, EditRoomType
from accounts.forms import SignUpForm, CreateManager
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import (
    staff_member_required,
)
from django.db.models import Q

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.admin.views.decorators import user_passes_test
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def superuser_required(
    view_func=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url="account_login_url",
):
    """
    Decorator for views that checks that the user is logged in and is a
    superuser, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


# Create your views here.
def home(request):
    rooms = Room.objects.all()
    form = FilterForm()
    bookings = Booking.objects.all()
    return render(
        request, "home.html", {"rooms": rooms, "bookings": bookings, "form": form}
    )


def filters(request):
    rooms = Room.objects.all()
    bookings = Booking.objects.all()

    if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            available = not form["show_only_available"].value()
            min_price = form["min_price"].value() if form["min_price"].value() else 0
            max_price = form["max_price"].value() if form["max_price"].value() else 1000
            beds = form["beds"].value() if form["beds"].value() else 0
            size = form["size"].value() if form["size"].value() else 0

            if not available:
                rooms = Room.objects.filter(
                    occupancy=available,
                    room_type__price__gte=min_price,
                    room_type__price__lte=max_price,
                    room_type__beds__gte=beds,
                    size__gte=size,
                )
                bookings = Booking.objects.filter(
                    room__occupancy=available,
                    room__room_type__price__gte=min_price,
                    room__room_type__price__lte=max_price,
                    room__room_type__beds__gte=beds,
                    room__size__gte=size,
                )
            else:
                rooms = Room.objects.filter(
                    room_type__price__gte=min_price,
                    room_type__price__lte=max_price,
                    room_type__beds__gte=beds,
                    size__gte=size,
                )
                bookings = Booking.objects.filter(
                    room__room_type__price__gte=min_price,
                    room__room_type__price__lte=max_price,
                    room__room_type__beds__gte=beds,
                    room__size__gte=size,
                )

            return render(
                request,
                "home.html",
                {"rooms": rooms, "bookings": bookings, "form": FilterForm()},
            )
    else:
        form = FilterForm()

    return render(
        request, "home.html", {"rooms": rooms, "bookings": bookings, "form": form}
    )


def book_rooms(request, id):
    room = Room.objects.get(pk=id)

    if request.method == "POST":

        form = BookingForm2(request.POST)

        if form.is_valid():
            date_from = form.cleaned_data["date_from"]
            date_to = form.cleaned_data["date_to"]
            current_user = request.user

            if current_user.is_authenticated:
                customer = Customer.objects.get(username=current_user.username)
                room.occupancy = True
                room.save()
                new_booking = Booking(
                    date_from=date_from,
                    date_to=date_to,
                    customer=customer,
                    room=room,
                )

                new_booking.save()

                to_pay = int((date_to - date_from).days * room.room_type.price)

                cc_number = form["card_number"].value()
                cc_expiry = form["card_expiry"].value()
                cc_code = form["card_code"].value()
                today = date.today()
                new_payment = Payment(
                    cc_number=cc_number,
                    cc_expiry=cc_expiry,
                    cc_code=cc_code,
                    customer=customer,
                    date=today,
                    amount=to_pay,
                )
                new_payment.save()

                return redirect("booking:home")

    else:
        form = BookingForm2()

    return render(request, "book_room.html", {"room": room, "form": form})


@staff_member_required(login_url="hotel:login")
def view_payments(request):
    payments = Payment.objects.all()
    return render(request, "view.html", {"payments": payments, "view_payment": True})


@staff_member_required(login_url="hotel:login")
def view_bookings(request):
    bookings = Booking.objects.all()
    return render(request, "view.html", {"bookings": bookings, "view_bookings": True})


@staff_member_required(login_url="hotel:login")
def view_room_types(request):
    room_types = Room_type.objects.all()
    return render(
        request, "view.html", {"room_types": room_types, "view_room_types": True}
    )


@staff_member_required(login_url="hotel:login")
def new_room(request):
    if request.method == "POST":

        form = AddRoom(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("booking:home")
    else:
        form = AddRoom()

    return render(request, "add_room.html", {"form": form})


@staff_member_required(login_url="hotel:login")
def remove_room(request, id):
    room = Room.objects.get(pk=id)
    room.delete()
    return redirect("booking:home")


@staff_member_required(login_url="hotel:login")
def remove_room_type(request, id):
    room_type = Room_type.objects.get(pk=id)
    room_type.delete()
    return redirect("booking:view_room_types")


@staff_member_required(login_url="hotel:login")
def remove_room_from_dashboard(request, id):
    room = Room.objects.get(pk=id)
    room.delete()
    return redirect("booking:rooms")


@staff_member_required(login_url="hotel:login")
def edit_room_type(request, id):
    room_type = Room_type.objects.get(pk=id)
    if request.method == "POST":

        form = EditRoomType(request.POST, request.FILES, instance=room_type)
        if form.is_valid():
            form.save()
            return redirect("booking:view_room_types")
    else:
        form = EditRoomType(instance=room_type)

    return render(
        request, "edit.html", {"form": form, "id": room_type.id, "edit": "Room_type"}
    )


@staff_member_required(login_url="hotel:login")
def edit_room(request, id):
    room = Room.objects.get(pk=id)

    if request.method == "POST":

        form = AddRoom(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect("booking:home")
    else:
        form = AddRoom(instance=room)

    return render(request, "edit.html", {"form": form, "id": room.id, "edit": "Room"})


@staff_member_required(login_url="hotel:login")
def customers(request):
    customers = Customer.objects.all()
    return render(request, "view.html", {"customers": customers, "customer": True})


@staff_member_required(login_url="hotel:login")
def rooms(request):
    rooms = Room.objects.all()
    return render(request, "view.html", {"rooms": rooms, "add_room": True})


@staff_member_required(login_url="hotel:login")
def edit_customers(request, id):
    customer = Customer.objects.get(pk=id)
    if request.method == "POST":

        form = EditCustomer(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("booking:customers")
    else:
        form = EditCustomer(instance=customer)

    return render(
        request, "edit.html", {"form": form, "id": customer.id, "edit": "Customer"}
    )


@staff_member_required(login_url="hotel:login")
def remove_customers(request, id):
    customer = Customer.objects.get(pk=id)
    u = User.objects.get(username=customer.username)
    u.delete()
    customer.delete()
    return redirect("booking:customers")


@staff_member_required(login_url="hotel:login")
def add_manager(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            first_name = form["first_name"].value()
            email = form["email"].value()
            last_name = form["last_name"].value()
            phone_number = form["phone_number"].value()
            username = form["username"].value()
            password = form["password1"].value()

            manager = Manager(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                username=username,
            )
            user = User.objects.create_user(username, email, password)
            user.is_staff = True
            user.save()

            manager.save()

            return redirect("booking:managers")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form, "manager": True})


@staff_member_required(login_url="hotel:login")
def managers(request):
    managers = Manager.objects.all()
    return render(request, "view.html", {"managers": managers, "add_manager": True})


@staff_member_required(login_url="hotel:login")
def edit_manager(request, id):
    manager = Manager.objects.get(pk=id)
    if request.method == "POST":

        form = EditCustomer(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect("booking:managers")
    else:
        form = EditCustomer(instance=manager)

    return render(
        request, "edit.html", {"form": form, "id": manager.id, "edit": "Manager"}
    )


@staff_member_required(login_url="hotel:login")
def remove_manager(request, id):
    manager = Manager.objects.get(pk=id)
    u = User.objects.get(username=manager.username)
    u.delete()
    manager.delete()
    return redirect("booking:managers")


@superuser_required(login_url="hotel:login")
def dashboard(request):
    return render(request, "dashboard.html")
