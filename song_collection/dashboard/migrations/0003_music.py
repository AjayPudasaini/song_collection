# Generated by Django 4.2.5 on 2023-09-25 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0002_alter_artist_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="Music",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                ("album_name", models.CharField(max_length=255, verbose_name="Album Name")),
                (
                    "genre",
                    models.CharField(
                        choices=[
                            ("rnb", "Rhythm and blues"),
                            ("country", "Country"),
                            ("classic", "Classic"),
                            ("rock", "Rock"),
                            ("jazz", "Jazz"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dashboard.artist", verbose_name="Artist"
                    ),
                ),
            ],
            options={
                "db_table": "Music",
            },
        ),
    ]
