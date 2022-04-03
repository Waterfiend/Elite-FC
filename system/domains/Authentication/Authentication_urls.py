from django.urls import path
import system.domains.Authentication.AuthenticationController as views


urlpatterns = [
    path('register/', views.renderRegistration),
    path('login', views.renderLogin),
    path('registerValidate/', views.validateRegistration),
    path('loginValidate/', views.validateLogin),
    path('Profile/', views.renderProfile),
    path('logout/',views.logout),
]