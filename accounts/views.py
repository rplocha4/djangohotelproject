from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from accounts.forms import SignUpForm
from .models import Customer
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import PasswordResetForm


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "registration/password_reset.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject"
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy("booking:home")


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


# def dashboard(request):
#     customers = Customer.objects.all()

#     return render(request, "dashboard.html", {"customers": customers})
