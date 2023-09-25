from django.urls import path

from song_collection.dashboard.views.artist import (
    ArtisrListView,
    ArtistCreateView,
    ArtistCSVExportView,
    ArtistCSVImportView,
    ArtistDeleteView,
    ArtistUpdateView,
)
from song_collection.dashboard.views.dashboard import DashboardView
from song_collection.dashboard.views.music import (
    MusicCreateView,
    MusicDeleteView,
    MusicListByArtist,
    MusicListView,
    MusicUpdateView,
)
from song_collection.dashboard.views.user import UserCreateView, UserDeleteView, UserListView, UserUpdateView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # user urls
    path("dashboard/user-create/", UserCreateView.as_view(), name="dashboard_user_create"),
    path("dashboard/user-lists/", UserListView.as_view(), name="dashboard_user_lists"),
    path("dashboard/user/<int:id>/update/", UserUpdateView.as_view(), name="dashboard_user_update"),
    path("dashboard/user/<int:id>/delete/", UserDeleteView.as_view(), name="dashboard_user_delete"),
    # artist urls
    path("dashboard/artist-lists/", ArtisrListView.as_view(), name="dashboard_artist_lists"),
    path("dashboard/artist-create/", ArtistCreateView.as_view(), name="dashboard_artist_create"),
    path("dashboard/artist/<int:id>/update/", ArtistUpdateView.as_view(), name="dashboard_artist_update"),
    path("dashboard/artist/<int:id>/delete/", ArtistDeleteView.as_view(), name="dashboard_artist_delete"),
    path("dashboard/artist-csv-import/", ArtistCSVImportView.as_view(), name="dashboard_artist_csv_import"),
    path("dashboard/artist-csv-export/", ArtistCSVExportView.as_view(), name="dashboard_artist_csv_export"),
    # music urls
    path("dashboard/music-create/", MusicCreateView.as_view(), name="dashboard_music_create"),
    path("dashboard/music-lists/", MusicListView.as_view(), name="dashboard_music_lists"),
    path("dashboard/music/<int:id>/update/", MusicUpdateView.as_view(), name="dashboard_music_update"),
    path("dashboard/music/<int:id>/delete/", MusicDeleteView.as_view(), name="dashboard_music_delete"),
    path("dashboard/artist/<int:id>/music/", MusicListByArtist.as_view(), name="dashboard_music_by_artist"),
]
