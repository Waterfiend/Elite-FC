from django.urls import path
import system.views as views

urlpatterns = [

    path('', views.hello),
    path('register/', views.renderRegistration),
    path('login', views.renderLogin),
    path('registerValidate/', views.validateRegistration),
    path('loginValidate/', views.validateLogin),
    path('Tickets/', views.renderTickets),
    path('TicketShop/', views.renderShop),
    path('CreateTicketForm/', views.createTicket),
    path('TicketValidate/', views.validateTicket),
    path('deleteTicket/<int:id>', views.deleteTicket),
    path('editTicket/<int:id>', views.editTicket),
    path('buyTicket/<int:id>', views.buyTicket),
    path('editTicketValidate/', views.editTicketValidate),
    path('Purchases/', views.purchases)
]
