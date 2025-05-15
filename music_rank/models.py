from django.db import models

# Create your models here.

class User(models):
    user_name = models.CharField(max_length=128)


class Song(models):
    song_name = models.CharField(max_length=128)
    song_url = models.CharField(max_length=128)

class UserHistory(models):
    user = models.ForeignKey(to=User)
    song = models.ForeignKey(to=Song)
    timestamp = models.DateTimeField()

