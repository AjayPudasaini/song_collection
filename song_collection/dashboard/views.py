from django.shortcuts import render, redirect
from django.views.generic import View


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        side_nav = "dashboard"
        context = {"side_nav":side_nav}
        return render(request, "dashboard/dashboard.html", context)
    

class UserListView(View):
    def get(self, request, *args, **kwargs):
        side_nav = "user"
        context = {"side_nav":side_nav}
        return render(request, "dashboard/users/user_list.html", context)