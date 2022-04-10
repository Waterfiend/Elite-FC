from django.urls import path
import system.domains.PlayerStat.PlayerStatController as views


urlpatterns = [
    path('PlayerStat/', views.HomeView.as_view(), name = "playerstat"),
    path('player/<int:pk>',views.PlayerDetailView.as_view(), name = 'player-detail'), #pk is the privatekey of each entry, each post  has its own unique primary key
    path('add_player/', views.AddPlayerView.as_view(), name = 'add_player'),
    path('player/edit/<int:pk>', views.UpdatePlayerView.as_view(), name = 'update_player'),
    path('player/<int:pk>/delete', views.DeletePlayerView.as_view(), name = 'delete_player'),
   
]