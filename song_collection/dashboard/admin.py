from django.contrib import admin

from song_collection.dashboard.models import Artist, Music

admin.site.register([Artist, Music])
