from django.urls import path
import system.domains.Tickets.TicketsController as views


urlpatterns = [
    path('Tickets/', views.renderTickets),
    path('CreateTicketForm/', views.createTicket),
    path('TicketValidate/', views.validateTicket),
    path('deleteTicket/<int:id>', views.deleteTicket),
    path('editTicket/<int:id>', views.editTicket),
    path('editTicketValidate/', views.editTicketValidate),
    path('ticketsShop/', views.ticketsShop),
    path('buyTicket/<int:id>', views.buyTicket),
]