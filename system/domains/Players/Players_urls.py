from django.urls import path
import system.domains.Players.PlayersController as views


urlpatterns = [
    path('Players/', views.renderPlayers),#render the players on the Player Matches page
    path('Matches/<int:id>', views.renderPlayerMatches),# renders the table of the player's matches
    path('playerStatisticsForm/<int:id>/<int:match_id>', views.playerStatisticsForm),# form used to add statistics for a player for a certain match
    path('editStatisticsValidate/<int:id>/<int:match_id>', views.editStatisticsValidate),# validate the statistics before commiting to database
    path('deleteStatistics/<int:id>/<int:match_id>', views.deleteStatistics),# delete a match statistic for a player
    
    
    path('PlayerStat/', views.HomeView.as_view(), name = "playerstat"),# render the players on the player Info page
    path('player/<int:pk>',views.PlayerDetailView.as_view(), name = 'player-detail'), #pk is the privatekey of each entry, each post  has its own unique primary key
    path('add_player/', views.AddPlayerView.as_view(), name = 'add_player'),
    path('player/edit/<int:pk>', views.UpdatePlayerView.as_view(), name = 'update_player'),
    path('player/<int:pk>/delete', views.DeletePlayerView.as_view(), name = 'delete_player'),
   
   #front end links
    path('viewPlayers/', views.FrontHomeView.as_view(), name = "playerview"),# render the players on the front end 
    path('playerstatisticsFront/<int:pk>', views.playerstatisticsFront.as_view(), name = "player-detailfront"),
]