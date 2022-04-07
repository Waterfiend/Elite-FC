from django.urls import path
import system.domains.Players.PlayersController as views


urlpatterns = [
    path('Players/', views.renderPlayers),
    path('Matches/<int:id>', views.renderPlayerMatches),
    path('playerStatisticsForm/<int:id>/<int:match_id>', views.playerStatisticsForm),
    path('editStatisticsValidate/<int:id>/<int:match_id>', views.editStatisticsValidate),
    path('deleteStatistics/<int:id>/<int:match_id>', views.deleteStatistics),
]