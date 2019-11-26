from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.intro, name='intro'),
    path('index/', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/reviews/', views.reviews, name='reviews'),
    path('<int:review_pk>/reviewupdate/', views.reviewupdate, name='reviewupdate'),
    path('<int:review_pk>/reviewdelete/', views.reviewdelete, name='reviewdelete'),
    path('addmovie/', views.addmovie, name='addmovie'),
    path('savemovie/', views.savemovie, name='savemovie'),
]
