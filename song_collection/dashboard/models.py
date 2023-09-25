import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from song_collection.utils.constant import GENDER_CHOICES, YEAR_CHOICES
from song_collection.utils.models import AbstractDateTime


class Artist(AbstractDateTime):
    name = models.CharField(_("Full Name"), blank=True, max_length=255)
    date_of_birth = models.DateField(_("Date Of Birth"), blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=5, choices=GENDER_CHOICES, default="M")
    address = models.CharField(
        _("Address"), max_length=255, help_text="Kathmandu, Bhaktpur, Lalitpur....", blank=True, null=True
    )
    first_release_year = models.PositiveIntegerField(
        choices=YEAR_CHOICES, default=datetime.date.today().year, verbose_name="First Released Year"
    )
    no_of_album_released = models.PositiveIntegerField(verbose_name="No of album released", default=1)

    class Meta:
        db_table = "Artist"
