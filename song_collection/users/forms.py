from django import forms
from django.core.validators import RegexValidator
from bootstrap_datepicker_plus.widgets import DatePickerInput

class RegisterForm(forms.Form):
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@])[A-Za-z\d@]{8,}$'
    password_validator = RegexValidator(
        password_regex,
        message="Password must be at least 8 characters and contain at least one uppercase letter, one number, and one '@' character."
    )

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone", max_length=15)
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=DatePickerInput(),
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select
    )
    address = forms.CharField(label="Address", help_text="Kathmandu, Bhaktpur, Lalitpur ...", max_length=100, required=False)

    password = forms.CharField(label="Password", widget=forms.PasswordInput, validators=[password_validator])
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
