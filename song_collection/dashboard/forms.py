from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms

from song_collection.utils.constant import GENDER_CHOICES


class UserUpdateForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone", max_length=15)
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=DatePickerInput(),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select)
    address = forms.CharField(
        label="Address", help_text="Kathmandu, Bhaktpur, Lalitpur ...", max_length=100, required=False
    )
