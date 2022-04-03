from django.urls import path, include
import system.views as views
urlpatterns = [
    path('', views.hello),
    
    path('',include('system.domains.Tickets.Tickets_urls')),
    path('',include('system.domains.Authentication.Authentication_urls')),
    path('',include('system.domains.ManageUsers.ManageUsers_urls')),
    path('',include('system.domains.FieldReservation.FieldReservation_urls')),
    path('',include('system.domains.ManagePermissions.ManagePermissions_urls')),

    path('accountSummary/', views.accountSummary),

]
