from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.shortcuts import redirect, render
from django.views.generic import View

from song_collection.dashboard.forms import ArtistCreateUpdateForm


class ArtisrListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            query = """SELECT * FROM "Artist" """
            cursor.execute(query)
            artist_data = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        side_nav = "artist"
        context = {"side_nav": side_nav, "artists": artist_data}
        return render(request, "dashboard/artist/artist_list.html", context)


class ArtistCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = ArtistCreateUpdateForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            name = cleaned_data.get("name")
            date_of_birth = cleaned_data.get("date_of_birth")
            gender = cleaned_data.get("gender")
            address = cleaned_data.get("address")
            first_release_year = cleaned_data.get("first_release_year")
            no_of_album_released = cleaned_data.get("no_of_album_released")
            current_date = datetime.now()

            with connection.cursor() as cursor:
                query = """
                        INSERT INTO "Artist"(name, date_of_birth, gender, address, first_release_year, no_of_album_released, created_at, updated_at)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                        """
                values = [
                    name,
                    date_of_birth,
                    gender,
                    address,
                    first_release_year,
                    no_of_album_released,
                    current_date,
                    current_date,
                ]
                cursor.execute(query, values)
                messages.success(request, "Artist created success")
            return redirect("dashboard_artist_lists")
        else:
            messages.info(request, "Artist Creation Failed")
            side_nav = "artist"
            context = {"side_nav": side_nav, "form": form}
            return render(request, "dashboard/artist/artist_create_update.html", context)

    def get(self, request, *args, **kwargs):
        form = ArtistCreateUpdateForm()
        side_nav = "artist"
        context = {"side_nav": side_nav, "form": form}
        return render(request, "dashboard/artist/artist_create_update.html", context)


class ArtistUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = ArtistCreateUpdateForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            updated_data = {
                "name": cleaned_data.get("name"),
                "date_of_birth": cleaned_data.get("date_of_birth"),
                "gender": cleaned_data.get("gender"),
                "address": cleaned_data.get("address"),
                "first_release_year": cleaned_data.get("first_release_year"),
                "no_of_album_released": cleaned_data.get("no_of_album_released"),
            }
            current_date = datetime.now()

            with connection.cursor() as cursor:
                query = """
                    UPDATE "Artist"
                    SET
                        name = %s,
                        date_of_birth = %s,
                        gender = %s,
                        address = %s,
                        first_release_year = %s,
                        no_of_album_released = %s,
                        updated_at = %s
                    WHERE id = %s
                """

                cursor.execute(
                    query,
                    [
                        updated_data.get("name"),
                        updated_data.get("date_of_birth"),
                        updated_data.get("gender"),
                        updated_data.get("address"),
                        updated_data.get("first_release_year"),
                        updated_data.get("no_of_album_released"),
                        current_date,
                        kwargs.get("id"),
                    ],
                )
                messages.success(request, "Artist updated success")
            return redirect("dashboard_artist_lists")
        else:
            messages.info(request, "Artist Update Failed")
            return redirect("dashboard_artist_lists")

    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            query = """
                SELECT id, name, date_of_birth, gender, address, first_release_year, no_of_album_released
                FROM "Artist"
                WHERE id = %s
            """
            cursor.execute(query, [kwargs.get("id")])
            artist_data = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
        form = ArtistCreateUpdateForm(
            initial={
                "name": artist_data.get("name"),
                "date_of_birth": artist_data.get("date_of_birth"),
                "gender": artist_data.get("gender"),
                "address": artist_data.get("address"),
                "first_release_year": artist_data.get("first_release_year"),
                "no_of_album_released": artist_data.get("no_of_album_released"),
            }
        )
        side_nav = "artist"
        context = {"side_nav": side_nav, "form": form}
        return render(request, "dashboard/artist/artist_create_update.html", context)


class ArtistDeleteView(View):
    def post(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                query = """DELETE FROM "Artist" WHERE id = %s"""
                cursor.execute(query, [kwargs.get("id")])
            messages.success(request, "Artist deletion success")
            return redirect("dashboard_artist_lists")
        except Exception as e:
            messages.info(request, f"Artist deletion Failed! {e}")
            return redirect("dashboard_artist_lists")
