from django.urls import path
import system.domains.FieldReservation.FieldReservationController as views

urlpatterns = [
    path('fieldReservation/', views.fieldReservation),
    path('reservationValidate/', views.reservationValidate),
    
    
    path('myReservations/', views.myReservations),
    path('refundReservation/<int:pk>', views.refundReservation),
]