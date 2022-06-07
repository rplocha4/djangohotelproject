from django import forms
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm
from .models import Room, Payment, Room_type
from accounts.models import Customer
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField

from bootstrap_datepicker_plus.widgets import DatePickerInput


class AddRoom(ModelForm):
    class Meta:
        model = Room
        fields = ["name", "room_type", "img", "size", "accesories"]


class EditCustomer(ModelForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget())

    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email", "phone_number"]


class EditRoomType(ModelForm):
    class Meta:
        model = Room_type
        fields = ["price", "beds"]


class FilterForm(forms.Form):
    show_only_available = forms.BooleanField(required=False)
    min_price = forms.FloatField(required=False, initial=0)
    max_price = forms.FloatField(required=False)
    beds = forms.IntegerField(required=False)
    size = forms.IntegerField(required=False)


class BookingForm2(forms.Form):
    date_from = forms.DateField(widget=DatePickerInput(format="%m/%d/%Y"))
    date_to = forms.DateField(widget=DatePickerInput(format="%m/%d/%Y"))

    card_number = forms.CharField(max_length=16)
    card_expiry = forms.CharField(max_length=5)
    card_code = forms.CharField(max_length=3)

    def clean(self):
        cd = self.cleaned_data

        if cd.get("date_from") >= cd.get("date_to"):
            self.add_error("date_to", "Date From must come before Date To")

            return cd
