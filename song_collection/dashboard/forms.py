import datetime
import os

from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.db import connection

from song_collection.utils.constant import GENDER_CHOICES, GENRE_CHOICES, YEAR_CHOICES


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


class ArtistCSVImportForm(forms.Form):
    file = forms.FileField(label="Select a file")

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")
        file_extension = os.path.splitext(file.name)[1].lower()
        if not file_extension == ".csv":
            self.add_error("file", "File extension must be CSV.")


class MusicCreateUpdateForm(forms.Form):
    artist = forms.ChoiceField(choices=[])
    title = forms.CharField(max_length=255)
    album_name = forms.CharField(max_length=255)
    genre = forms.ChoiceField(choices=GENRE_CHOICES, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["artist"].choices = self.get_artist_choices()

    def get_artist_choices(self):
        with connection.cursor() as cursor:
            query = """ SELECT id, name FROM "Artist" """
            cursor.execute(query)
            artist_data = cursor.fetchall()
        return artist_data
