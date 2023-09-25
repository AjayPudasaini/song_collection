from datetime import datetime

from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django.db import connection
from django.shortcuts import redirect, render
from django.views.generic import View

from song_collection.dashboard.forms import MusicCreateUpdateForm
from song_collection.utils.mixin import SuperuserRequiredMixin


class MusicCreateView(SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = MusicCreateUpdateForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            artist_id = cleaned_data["artist"]
            title = cleaned_data["title"]
            album_name = cleaned_data["album_name"]
            genre = cleaned_data["genre"]
            current_date = datetime.now()

            with connection.cursor() as cursor:
                query = """
                        INSERT INTO "Music"(artist_id, title, album_name, genre, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)
                        """

                cursor.execute(query, [artist_id, title, album_name, genre, current_date, current_date])

            return redirect("dashboard_music_lists")
        else:
            return render(request, "dashboard/song/song_create_update.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = MusicCreateUpdateForm()
        side_nav = "music"
        context = {"side_nav": side_nav, "form": form}
        return render(request, "dashboard/song/song_create_update.html", context)


class MusicListView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        page_number = request.GET.get("page", 1)
        per_page = 5

        with connection.cursor() as cursor:
            query = """SELECT * FROM "Music" """
            cursor.execute(query)
            music_data = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

        paginator = Paginator(music_data, per_page)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        side_nav = "music"
        context = {"side_nav": side_nav, "songs": page}
        return render(request, "dashboard/song/song_list.html", context)


class MusicUpdateView(SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = MusicCreateUpdateForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            updated_data = {
                "artist": cleaned_data.get("artist"),
                "title": cleaned_data.get("title"),
                "album_name": cleaned_data.get("album_name"),
                "genre": cleaned_data.get("genre"),
            }
            current_date = datetime.now()

            with connection.cursor() as cursor:
                query = """
                    UPDATE "Music"
                    SET
                        artist_id = %s,
                        title = %s,
                        album_name = %s,
                        genre = %s,
                        updated_at = %s
                    WHERE id = %s
                """

                cursor.execute(
                    query,
                    [
                        updated_data.get("artist"),
                        updated_data.get("title"),
                        updated_data.get("album_name"),
                        updated_data.get("genre"),
                        current_date,
                        kwargs.get("id"),
                    ],
                )
                messages.success(request, "Music updated success")
            return redirect("dashboard_music_lists")
        else:
            messages.info(request, "Music Update Failed")
            return redirect("dashboard_music_lists")

    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            query = """
                SELECT id, artist_id, title, album_name, genre
                FROM "Music"
                WHERE id = %s
            """
            cursor.execute(query, [kwargs.get("id")])
            music_data = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
        form = MusicCreateUpdateForm(
            initial={
                "artist_id": music_data.get("artist_id"),
                "title": music_data.get("title"),
                "album_name": music_data.get("album_name"),
                "genre": music_data.get("genre"),
            }
        )
        side_nav = "music"
        context = {"side_nav": side_nav, "form": form}
        return render(request, "dashboard/song/song_create_update.html", context)


class MusicDeleteView(SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                query = """DELETE FROM "Music" WHERE id = %s"""
                cursor.execute(query, [kwargs.get("id")])
            messages.success(request, "Music deletion success")
            return redirect("dashboard_music_lists")
        except Exception as e:
            messages.info(request, f"Music deletion Failed! {e}")
            return redirect("dashboard_music_lists")


class MusicListByArtist(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        page_number = request.GET.get("page", 1)
        per_page = 5
        with connection.cursor() as cursor:
            query = """SELECT * FROM "Music"  WHERE artist_id = %s"""
            cursor.execute(query, [kwargs.get("id")])
            music_data = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

        paginator = Paginator(music_data, per_page)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        side_nav = "music"
        context = {"side_nav": side_nav, "songs": page}
        return render(request, "dashboard/song/song_list.html", context)
