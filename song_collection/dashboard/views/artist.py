from datetime import datetime

import pandas as pd
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, Paginator
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from song_collection.dashboard.forms import ArtistCreateUpdateForm, ArtistCSVImportForm


class ArtisrListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        page_number = request.GET.get("page", 1)
        per_page = 5

        with connection.cursor() as cursor:
            query = """SELECT * FROM "Artist" """
            cursor.execute(query)
            artist_data = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

        paginator = Paginator(artist_data, per_page)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        side_nav = "artist"
        context = {"side_nav": side_nav, "artists": page}
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


class ArtistCSVImportView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = ArtistCSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data.get("file")
            df = pd.read_csv(file, dtype=str)
            if df.isnull().values.any():
                form.add_error("file", "All CSV fields are required")
                side_nav = "artist"
                context = {"side_nav": side_nav, "form": form}
                return render(request, "dashboard/artist/artist_import.html", context)
            data_to_insert = []
            for ind in df.index:
                id = df.get("id")[ind]
                name = df.get("name")[ind]
                date_of_birth = df.get("date_of_birth")[ind]
                gender = df.get("gender")[ind]
                address = df.get("address")[ind]
                first_release_year = df.get("first_release_year")[ind]
                no_of_album_released = df.get("no_of_album_released")[ind]
                current_date = datetime.now()

                with connection.cursor() as cursor:
                    query = """SELECT id FROM "Artist" WHERE id = %s"""
                    cursor.execute(query, [str(id)])
                    artist_data = cursor.fetchone()
                if artist_data:
                    messages.info(request, "CSV import is for adding new data only, updates are not supported.")
                    side_nav = "artist"
                    context = {"side_nav": side_nav, "form": form}
                    return render(request, "dashboard/artist/artist_import.html", context)

                data_to_insert.append(
                    [
                        name,
                        date_of_birth,
                        gender,
                        address,
                        first_release_year,
                        no_of_album_released,
                        current_date,
                        current_date,
                    ]
                )

            if data_to_insert:
                insert_query = """
                        INSERT INTO "Artist" (name, date_of_birth, gender, address, first_release_year, no_of_album_released, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """

                with connection.cursor() as cursor:
                    for i in data_to_insert:
                        cursor.execute(insert_query, i)

                messages.success(request, "CSV Imported Success")
            return redirect("dashboard_artist_lists")
        else:
            messages.info(request, "CSV Import failed.")
            side_nav = "artist"
            context = {"side_nav": side_nav, "form": form}
            return render(request, "dashboard/artist/artist_import.html", context)

    def get(self, request, *args, **kwargs):
        form = ArtistCSVImportForm()
        side_nav = "artist"
        context = {"side_nav": side_nav, "form": form}
        return render(request, "dashboard/artist/artist_import.html", context)


class ArtistCSVExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = """
            SELECT id, name, date_of_birth, gender, address, first_release_year, no_of_album_released, created_at, updated_at
            FROM "Artist"
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()

        columns = [
            "id",
            "name",
            "date_of_birth",
            "gender",
            "address",
            "first_release_year",
            "no_of_album_released",
            "created_at",
            "updated_at",
        ]
        df = pd.DataFrame(data, columns=columns)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="artists.csv"'
        df.to_csv(response, index=False)
        return response
