from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from accounts.forms import SignUpForm
from .models import Customer


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form["first_name"].value()
            email = form["email"].value()
            last_name = form["last_name"].value()
            phone_number = form["phone_number"].value()
            username = form["username"].value()
            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                username=username,
            )
            customer.save()
            return redirect("hotel:login")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def dashboard(request):
    customers = Customer.objects.all()

    return render(request, "dashboard.html", {"customers": customers})


