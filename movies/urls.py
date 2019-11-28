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
    path('movielevellist/', views.movielevellist, name='movielevellist'),
    path('addmovie/', views.addmovie, name='addmovie'),
    path('savemovie/', views.savemovie, name='savemovie'),
    # 영화 수정 삭제용
    # path('<int:movie_pk>/updatemovie/', views.updatemovie, name='updatemovie'),
    # path('<int:movie_pk>/deletemovie/', views.deletemovie, name='deletemovie'),
    path('recommendation/', views.recommendation, name='recommendation'),
    path('recommendlist/', views.recommendlist, name='recommendlist'),
]
