from django.urls import path

from song_collection.dashboard.views.artist import ArtisrListView, ArtistCreateView, ArtistDeleteView, ArtistUpdateView
from song_collection.dashboard.views.dashboard import DashboardView
from song_collection.dashboard.views.user import UserDeleteView, UserListView, UserUpdateView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/user-lists/", UserListView.as_view(), name="dashboard_user_lists"),
    path("dashboard/user/<int:id>/update/", UserUpdateView.as_view(), name="dashboard_user_update"),
    path("dashboard/user/<int:id>/delete/", UserDeleteView.as_view(), name="dashboard_user_delete"),
    # artist urls
    path("dashboard/artist-lists/", ArtisrListView.as_view(), name="dashboard_artist_lists"),
    path("dashboard/artist-create/", ArtistCreateView.as_view(), name="dashboard_artist_create"),
    path("dashboard/artist/<int:id>/update/", ArtistUpdateView.as_view(), name="dashboard_artist_update"),
    path("dashboard/artist/<int:id>/delete/", ArtistDeleteView.as_view(), name="dashboard_artist_delete"),
]
