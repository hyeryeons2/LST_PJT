from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('update/password/', views.password, name='password'), 
    path('liguild/', views.liguild, name='liguild'),
    path('mkguild/', views.mkguild, name='mkguild'), 
    path('joinguild/<int:guild_pk>/', views.joinguild, name='joinguild'), 
    path('leaveguild/', views.leaveguild, name='leaveguild'), 
]
