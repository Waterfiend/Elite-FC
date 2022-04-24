from django.urls import path
import system.domains.Authentication.AuthenticationController as views


urlpatterns = [
    path('register/', views.renderRegistration),# takes user to registration form
    path('login', views.renderLogin),# takes user to login form
    path('registerValidate/', views.validateRegistration),#validate the registration information entered by the user
    path('loginValidate/', views.validateLogin),#validate the login information entered by the user
    path('Profile/', views.renderProfile),#renders the user profile page 
    path('logout/',views.logout),#ends user session
    path('changePasswordandEmailForm/',views.changePasswordandEmailForm),# show change email and password form
    path('validatePassword/',views.validatePassword),# validate new email and password
]