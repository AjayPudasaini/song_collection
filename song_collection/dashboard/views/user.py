from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, Paginator
from django.db import connection
from django.shortcuts import redirect, render
from django.views.generic import View

from song_collection.dashboard.forms import UserUpdateForm
from song_collection.users.forms import RegisterForm
from song_collection.utils.utils import user_create


class UserCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user_create(request, cleaned_data)
            return redirect("dashboard_user_lists")
        else:
            return render(request, "dashboard/users/user_create.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {"form": form}
        return render(request, "dashboard/users/user_create.html", context)


class UserListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        page_number = request.GET.get("page", 1)
        per_page = 5
        with connection.cursor() as cursor:
            query = """SELECT * FROM "User" """
            cursor.execute(query)
            user_data = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        paginator = Paginator(user_data, per_page)
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        side_nav = "user"
        context = {"side_nav": side_nav, "users": page}
        return render(request, "dashboard/users/user_list.html", context)


class UserUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            updated_data = {
                "first_name": cleaned_data.get("first_name"),
                "last_name": cleaned_data.get("last_name"),
                "email": cleaned_data.get("email"),
                "phone": cleaned_data.get("phone"),
                "date_of_birth": cleaned_data.get("date_of_birth"),
                "gender": cleaned_data.get("gender"),
                "address": cleaned_data.get("address"),
            }
            current_date = datetime.now()
            with connection.cursor() as cursor:
                query = """
                    UPDATE "User"
                    SET
                        first_name = %s,
                        last_name = %s,
                        email = %s,
                        phone = %s,
                        date_of_birth = %s,
                        gender = %s,
                        address = %s,
                        updated_at = %s
                    WHERE id = %s
                """
                cursor.execute(
                    query,
                    [
                        updated_data.get("first_name"),
                        updated_data.get("last_name"),
                        updated_data.get("email"),
                        updated_data.get("phone"),
                        updated_data.get("date_of_birth"),
                        updated_data.get("gender"),
                        updated_data.get("address"),
                        current_date,
                        kwargs.get("id"),
                    ],
                )
            return redirect("dashboard_user_lists")
        else:
            messages.info(request, "User update failed.")
            return redirect("dashboard_user_update", kwargs.get("id"))

    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            query = """
                SELECT id, first_name, last_name, email, phone, date_of_birth, gender, address
                FROM "User"
                WHERE id = %s
            """
            cursor.execute(query, [kwargs.get("id")])
            user_data = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
        form = UserUpdateForm(
            initial={
                "first_name": user_data.get("first_name"),
                "last_name": user_data.get("last_name"),
                "email": user_data.get("email"),
                "phone": user_data.get("phone"),
                "date_of_birth": user_data.get("date_of_birth"),
                "gender": user_data.get("gender"),
                "address": user_data.get("address"),
            }
        )
        side_nav = "user"
        context = {"side_nav": side_nav, "form": form}
        return render(request, "dashboard/users/user_update.html", context)


class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                query = """DELETE FROM "User" WHERE id = %s"""
                cursor.execute(query, [kwargs.get("id")])
            messages.success(request, "User deletion success")
            return redirect("dashboard_user_lists")
        except Exception as e:
            messages.info(request, f"User deletion Failed! {e}")
            return redirect("dashboard_user_lists")
