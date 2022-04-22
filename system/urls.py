from django.urls import path, include
import system.views as views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.hello),
    
    path('',include('system.domains.Tickets.Tickets_urls')),
    path('',include('system.domains.Authentication.Authentication_urls')),
    path('',include('system.domains.ManageUsers.ManageUsers_urls')),
    path('',include('system.domains.FieldReservation.FieldReservation_urls')),
    path('',include('system.domains.ManagePermissions.ManagePermissions_urls')),
    path('',include('system.domains.News.News_urls')),
    path('',include('system.domains.Matches.Matches_urls')),
    path('',include('system.domains.Players.Players_urls')),
    path('',include('system.domains.FeesSalaries.FeesSalaries_urls')),
    path('',include('system.domains.Reports.Reports_urls')),
    path('',include('system.domains.Teams.Teams_urls')),
    path('accountSummary/', views.accountSummary),
    path('tierEnrollment/', views.tierEnrollment),
    path('tierSelection/<int:id>', views.tierSelection),
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
