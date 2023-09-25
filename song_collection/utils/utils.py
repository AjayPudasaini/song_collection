from datetime import datetime

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db import connection


def user_create(request, cleaned_data):
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
