from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DashboardConfig(AppConfig):
    name = "song_collection.dashboard"
    verbose_name = _("Dashboard")
