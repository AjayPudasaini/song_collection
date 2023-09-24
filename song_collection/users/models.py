from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from song_collection.utils.models import AbstractDateTime
from song_collection.users.managers import CustomUserManager
from song_collection.utils.constant import GENDER_CHOICES

class User(AbstractUser, AbstractDateTime):
    """
    Default custom user model for song_collection.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.
    """

    first_name = models.CharField(_("First Name"), blank=True, max_length=255)
    last_name = models.CharField(_("Last Name"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(_("Phone"), blank=True, max_length=15)
    date_of_birth = models.DateField(_("Date Of Birth"), blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=5, choices=GENDER_CHOICES, default="M")
    address = models.CharField(_("Address"), max_length=255, help_text="Kathmandu, Bhaktpur, Lalitpur....", blank=True, null=True)

    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    class Meta:
        db_table="User"