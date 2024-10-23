from django.urls import path
from .import views

app_name = 'animes_by_community'    
urlpatterns= [
    path('create/', views.create_anime, name = 'create_anime'),
    path('show/', views.show_animes_by_community, name = 'show_animes_by_community'),
    path('manage/', views.manage_animes_by_me, name = 'manage_animes_by_me'),
]