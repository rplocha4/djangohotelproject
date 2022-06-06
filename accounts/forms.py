from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from phonenumber_field.modelfields import PhoneNumberField
from .models import Manager
from django.forms import ModelForm


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "input", "placeholder": "Your username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "input", "placeholder": "Your password"}
        )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Optional",
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Optional",
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )
    email = forms.EmailField(
        max_length=254,
        help_text="Enter a valid email address",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )
    phone_number = forms.RegexField(
        regex=r"^\+?1?\d{9,15}$",
        widget=forms.TextInput(attrs={"placeholder": "Phone number"}),
        error_messages={"invalid": "Enter a valid phone number."},
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password again"}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]


class CreateManager(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Manager
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]
