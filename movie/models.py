from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    email = None
    nickname = models.CharField(max_length=100)

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    title_kor = models.CharField(max_length=100)
    title_eng = models.TextField(default='')
    poster_url = models.URLField(max_length=1024)
    genre = models.CharField(max_length=100, blank=True)
    showtime = models.CharField(max_length=30, blank=True)
    release_date = models.TextField(default='', blank=True)
    plot = models.TextField(default='', blank=True)
    rating = models.CharField(max_length=50)
    director_name = models.CharField(max_length=100)
    director_image_url = models.URLField(max_length=1024, null=True)

    def __str__(self):
        return self.title_kor

class Actor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='actors')
    name = models.CharField(max_length=100)
    character = models.CharField(max_length=500, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)