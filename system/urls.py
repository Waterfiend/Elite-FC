from django.urls import path
import system.views as views

urlpatterns = [

    path('', views.hello),
    path('register/', views.renderRegistration),
    path('login', views.renderLogin),
    path('registerValidate/', views.validateRegistration),
    path('loginValidate/', views.validateLogin),
    path('Tickets/', views.renderTickets),
    path('CreateTicketForm/', views.createTicket),
    path('TicketValidate/', views.validateTicket),
    path('deleteTicket/<int:id>', views.deleteTicket),
]
