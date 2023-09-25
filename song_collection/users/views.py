from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.db import connection
from django.shortcuts import redirect, render
from django.views.generic import View

from song_collection.users.forms import LoginForm, RegisterForm
from song_collection.utils.utils import user_create


class UserRegisterView(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user_create(request, cleaned_data, superuser=True, staff=True)
            return redirect("user_login")
        else:
            return render(request, "users/auth/register.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {"form": form}
        return render(request, "users/auth/register.html", context)


class UserLoginView(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            with connection.cursor() as cursor:
                query = """SELECT email, password FROM "User" WHERE email = %s AND is_superuser=True """
                cursor.execute(query, [email])
                user_data = cursor.fetchone()

            if user_data:
                user_id, hashed_password = user_data
                if check_password(password, hashed_password):
                    user = authenticate(request, email=email, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect("dashboard")
            else:
                messages.info(request, "Invalid Email and password")

        context = {"form": form, "message": "Login"}
        return render(request, "users/auth/login.html", context)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        form = LoginForm()
        context = {"form": form, "message": "Login"}
        return render(request, "users/auth/login.html", context)
