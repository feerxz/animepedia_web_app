from django.urls import path
from .import views

urlpatterns= [
    path('', views.home, name = 'home'),
    path('login/', views.login_, name = 'login'),
    path('animes/', views.animes, name = 'animes'),
    path('signup/', views.signup, name = 'signup'),
    path('signout/', views.signout, name = 'signout'),
    path('browse/', views.browse_animes, name = 'browse_animes'),
    path('anime/<int:anime_id>/', views.anime_detail, name = 'anime_detail'),
    path('movies/', views.anime_movies, name = 'anime_movies'),
    path('series/', views.anime_series, name = 'anime_series'),
    path('createfavorites/', views.favorites_list, name = 'create_favorites_list'),
    path('myaccount/',views.my_account, name = 'my_account'),
    path('myaccount/profile/',views.profile, name = 'profile'),
    path('myaccount/profile/changepassword/', views.change_password, name='change_password'),
    path('myaccount/mylists/',views.manage_favorites_lists, name = 'manage_favorites_lists'),
    path('myaccount/mylists/<int:list_id>/',views.list_detail, name = 'list_detail'),
    path('myaccount/mylists/<int:list_id>/edit/',views.list_edit, name = 'list_edit'),
    
]