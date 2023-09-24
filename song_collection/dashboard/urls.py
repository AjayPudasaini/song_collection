from django.urls import path

from song_collection.dashboard.views import DashboardView, UserDeleteView, UserListView, UserUpdateView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/user-lists/", UserListView.as_view(), name="dashboard_user_lists"),
    path("dashboard/user/<int:id>/update/", UserUpdateView.as_view(), name="dashboard_user_update"),
    path("dashboard/user/<int:id>/delete/", UserDeleteView.as_view(), name="dashboard_user_delete"),
]
