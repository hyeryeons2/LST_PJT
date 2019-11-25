from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.intro, name='intro'),
    path('index/', views.index, name='index'),
    path('addmovie/', views.addmovie, name='addmovie'),
]
