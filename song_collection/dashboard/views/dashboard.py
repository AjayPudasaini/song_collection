from django.shortcuts import render
from django.views.generic import View

from song_collection.utils.mixin import SuperuserRequiredMixin


class DashboardView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        side_nav = "dashboard"
        context = {"side_nav": side_nav}
        return render(request, "dashboard/dashboard.html", context)
