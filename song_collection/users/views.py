from django.shortcuts import render
from django.views.generic import View

class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        message = "Test Message"
        context = {"message": message}
        return render(request, "users/auth/login.html", context)