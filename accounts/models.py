from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Guild(models.Model):
    name = models.CharField(max_length=40)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)


class User(AbstractUser):
    # username = models.CharField(max_length=30, unique=True,
    #     help_text=_()
    # )
    # passwrod = 
    nickname = models.CharField(max_length=20)
    age = models.IntegerField(blank=True, null=True)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followings' 
    )
    group = models.ForeignKey(Guild, related_name='member', on_delete=models.SET_NULL, blank=True, null=True)
