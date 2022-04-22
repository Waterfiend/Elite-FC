from django.urls import path
import system.domains.Teams.TeamsController as views


urlpatterns = [
    path('Teams/', views.HomeView.as_view(), name = "teams"),
    path('team/<int:pk>',views.TeamDetailView.as_view(), name = 'team-detail'), 
    path('add_team/', views.AddTeamView.as_view(), name = 'add_team'),
    path('team/edit/<int:pk>', views.UpdateTeamView.as_view(), name = 'update_team'),
    path('team/<int:pk>/delete', views.DeleteTeamView.as_view(), name = 'delete_team'),
]