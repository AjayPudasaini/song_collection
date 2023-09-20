from django.urls import path
from song_collection.users.views import UserLoginView


urlpatterns = [
    path("", UserLoginView.as_view(), name="user_login"),
]
