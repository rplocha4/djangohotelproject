from django import forms
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm
from .models import Room
from accounts.models import Customer
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField


class BookingForm(forms.Form):
    date_from = forms.DateField(
        initial=datetime.date.today,
        widget=AdminDateWidget(
            attrs={"class": "date-field", "data-date-format": "dd/mm/yyyy"}
        ),
    )
    date_to = forms.DateField(
        initial=datetime.date.today,
        widget=AdminDateWidget(
            attrs={"class": "date-field", "data-date-format": "dd/mm/yyyy"}
        ),
    )


class AddRoom(ModelForm):
    class Meta:
        model = Room
        fields = ["name", "room_type", "img", "size", "accesories"]


class EditCustomer(ModelForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget())

    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email", "phone_number"]


class FilterForm(forms.Form):
    show_only_available = forms.BooleanField(required=False)
    min_price = forms.FloatField(required=False, initial=0)
    max_price = forms.FloatField(required=False)
    beds = forms.IntegerField(required=False)
    size = forms.IntegerField(required=False)
