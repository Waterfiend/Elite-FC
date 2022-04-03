from django.urls import path
import system.domains.Matches.MatchesController as views


urlpatterns = [
    path('schedule/', views.display_schedule),
    path('deletematch/<int:match_id>', views.delete_match),
    path('editmatch/<int:match_id>', views.display_matchform),
    path('postmatch/<int:match_id>', views.post_match),
]