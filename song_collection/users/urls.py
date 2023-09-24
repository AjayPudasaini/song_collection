from django.contrib.auth.views import LogoutView
from django.urls import path

from song_collection.users.views import UserLoginView, UserRegisterView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("", UserLoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
