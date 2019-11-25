from django.db import models
from django.conf import settings


class Movie(models.Model):
    title = models.CharField(max_length=50)
    title_en = models.CharField(max_length=100)
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=140)
    description = models.TextField()
    running_time = models.CharField(max_length=30)
    directors = models.CharField(max_length=100)
    actors = models.CharField(max_length=100)
    watch_grade = models.CharField(max_length=30)
    level = models.IntegerField()
    review_link = models.CharField(max_length=200)
    preview_link = models.CharField(max_length=200)
    genres = models.CharField(max_length=100)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies')
    recommend_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)


class Review(models.Model):
    content = models.CharField(max_length=140)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
