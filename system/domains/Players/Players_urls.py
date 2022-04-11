from django.urls import path
import system.domains.Players.PlayersController as views


urlpatterns = [
    path('Players/', views.renderPlayers),
    path('Matches/<int:id>', views.renderPlayerMatches),
    path('playerStatisticsForm/<int:id>/<int:match_id>', views.playerStatisticsForm),
    path('editStatisticsValidate/<int:id>/<int:match_id>', views.editStatisticsValidate),
    path('deleteStatistics/<int:id>/<int:match_id>', views.deleteStatistics),
    
    
    path('PlayerStat/', views.HomeView.as_view(), name = "playerstat"),
    path('player/<int:pk>',views.PlayerDetailView.as_view(), name = 'player-detail'), #pk is the privatekey of each entry, each post  has its own unique primary key
    path('add_player/', views.AddPlayerView.as_view(), name = 'add_player'),
    path('player/edit/<int:pk>', views.UpdatePlayerView.as_view(), name = 'update_player'),
    path('player/<int:pk>/delete', views.DeletePlayerView.as_view(), name = 'delete_player'),
   
]