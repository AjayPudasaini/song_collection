import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms

from song_collection.utils.constant import GENDER_CHOICES, YEAR_CHOICES


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


class ArtistCreateUpdateForm(forms.Form):
    name = forms.CharField(label="Name")
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=DatePickerInput(),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select)
    address = forms.CharField(
        label="Address", help_text="Kathmandu, Bhaktpur, Lalitpur ...", max_length=100, required=False
    )
    first_release_year = forms.ChoiceField(
        choices=YEAR_CHOICES, widget=forms.Select, initial=datetime.date.today().year, label="First release year"
    )
    no_of_album_released = forms.IntegerField(
        widget=forms.NumberInput(attrs={"type": "number", "min": "0"}), label="No of album released"
    )
