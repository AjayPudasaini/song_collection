import datetime

GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]

YEAR_CHOICES = [(year, year) for year in range(datetime.date.today().year, 1900, -1)]

GENRE_CHOICES = [
    ("rnb", "Rhythm and blues"),
    ("country", "Country"),
    ("classic", "Classic"),
    ("rock", "Rock"),
    ("jazz", "Jazz"),
]
