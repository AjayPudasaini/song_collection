from django.urls import path
from song_collection.users.views import UserRegisterView, UserLoginView


urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("", UserLoginView.as_view(), name="user_login"),
]
