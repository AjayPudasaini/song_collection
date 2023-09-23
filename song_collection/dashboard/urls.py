from django.urls import path
from song_collection.dashboard.views import DashboardView, UserListView


urlpatterns = [
   path("dashboard/", DashboardView.as_view(), name="dashboard"),
   path("dashboard/user-lists/", UserListView.as_view(), name="dashboard_user_lists"),
]
