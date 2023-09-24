from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password
from django.db import connection
from django.shortcuts import redirect, render
from django.views.generic import View

from song_collection.users.forms import LoginForm, RegisterForm


class UserRegisterView(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            first_name = cleaned_data.get("first_name")
            last_name = cleaned_data.get("last_name")
            email = cleaned_data.get("email")
            phone = cleaned_data.get("phone")
            date_of_birth = cleaned_data.get("date_of_birth")
            gender = cleaned_data.get("gender")
            address = cleaned_data.get("address")
            password = make_password(cleaned_data.get("password"))
            is_superuser = False
            is_staff = False
            is_active = True
            current_date = datetime.now()

            with connection.cursor() as cursor:
                query = """ SELECT COUNT(*) FROM "User" WHERE email = %s """
                cursor.execute(query, [email])
                email_count = cursor.fetchone()[0]

            if email_count > 0:
                form.add_error("email", "This email is already registered.")
                return render(request, "users/auth/register.html", {"form": form})

            with connection.cursor() as cursor:
                query = """
                        INSERT INTO "User"(first_name, last_name, email, phone, date_of_birth, gender, address, password, is_superuser, is_staff, is_active, date_joined, created_at, updated_at)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                values = [
                    first_name,
                    last_name,
                    email,
                    phone,
                    date_of_birth,
                    gender,
                    address,
                    password,
                    is_superuser,
                    is_staff,
                    is_active,
                    current_date,
                    current_date,
                    current_date,
                ]
                cursor.execute(query, values)
                messages.success(request, "User created success")
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
                query = """SELECT email, password FROM "User" WHERE email = %s"""
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
        form = LoginForm()
        context = {"form": form, "message": "Login"}
        return render(request, "users/auth/login.html", context)
