from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=128)


class Song(models.Model):
    song_name = models.CharField(max_length=128)
    song_url = models.CharField(max_length=128)


