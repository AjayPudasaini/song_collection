from django.shortcuts import render, redirect
from django.views.generic import View
from song_collection.users.forms import RegisterForm, LoginForm


class UserRegisterView(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            return redirect('user_login')
        else:
            return render(request, "users/auth/register.html", {"form": form, "message": "Register"})

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {"form": form, "message":"Register"}
        return render(request, "users/auth/register.html", context)


class UserLoginView(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            if email == "ajayapudasaini999@gmail.com" and password == "1530":
                return redirect('dashboard')
            else:
                form.add_error("email", "Invalid email or password")
                form.add_error("password", "Invalid email or password")
        context = {"form": form, "message": "Login"}
        return render(request, "users/auth/login.html", context)

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {"form": form, "message":"Login"}
        return render(request, "users/auth/login.html", context)