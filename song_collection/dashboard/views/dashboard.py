from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        side_nav = "dashboard"
        context = {"side_nav": side_nav}
        return render(request, "dashboard/dashboard.html", context)
