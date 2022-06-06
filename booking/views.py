from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Room, Booking
from accounts.models import Customer, Manager
from .forms import BookingForm, AddRoom, EditCustomer, FilterForm
from accounts.forms import SignUpForm, CreateManager
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q

# from accounts.forms import CreateManager


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


def rooms(request, id):
    room = Room.objects.get(pk=id)

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():
            date_from = form.cleaned_data["date_from"]
            date_to = form.cleaned_data["date_to"]
            current_user = request.user

            if current_user.is_authenticated:
                customer = Customer.objects.get(username=current_user.username)
                new_booking = Booking(
                    date_from=date_from,
                    date_to=date_to,
                    customer=customer,
                    room=room,
                )
                room.occupancy = True
                room.save()
                new_booking.save()
                return redirect("booking:home")
    else:
        form = BookingForm()

    return render(request, "rooms.html", {"room": room, "form": form})


@staff_member_required
def new_room(request):
    if request.method == "POST":

        form = AddRoom(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("booking:home")
    else:
        form = AddRoom()

    return render(request, "add_room.html", {"form": form})


@staff_member_required
def remove_room(request, id):
    room = Room.objects.get(pk=id)
    room.delete()
    return redirect("booking:home")


@staff_member_required
def edit_room(request, id):
    room = Room.objects.get(pk=id)

    if request.method == "POST":

        form = AddRoom(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect("booking:home")
    else:
        form = AddRoom(instance=room)

    return render(request, "edit.html", {"form": form})


@staff_member_required
def customers(request):
    customers = Customer.objects.all()
    return render(request, "view.html", {"customers": customers})


@staff_member_required
def edit_customers(request, id):
    customer = Customer.objects.get(pk=id)
    if request.method == "POST":

        form = EditCustomer(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("booking:customers")
    else:
        form = EditCustomer(instance=customer)

    return render(request, "edit.html", {"form": form})


@staff_member_required
def remove_customers(request, id):
    customer = Customer.objects.get(pk=id)
    u = User.objects.get(username=customer.username)
    u.delete()
    customer.delete()
    return redirect("booking:customers")


@staff_member_required
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


@staff_member_required
def managers(request):
    managers = Manager.objects.all()
    return render(request, "view.html", {"managers": managers, "add_manager": True})


@staff_member_required
def edit_manager(request, id):
    manager = Manager.objects.get(pk=id)
    if request.method == "POST":

        form = EditCustomer(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect("booking:customers")
    else:
        form = EditCustomer(instance=manager)

    return render(request, "edit.html", {"form": form})


@staff_member_required
def remove_manager(request, id):
    manager = Manager.objects.get(pk=id)
    u = User.objects.get(username=manager.username)
    u.delete()
    manager.delete()
    return redirect("booking:managers")
