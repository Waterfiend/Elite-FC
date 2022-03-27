from django.urls import path
import system.views as views

urlpatterns = [
    path('', views.hello),
    path('register/', views.renderRegistration),
    path('login', views.renderLogin),
    path('registerValidate/', views.validateRegistration),
    path('loginValidate/', views.validateLogin),
    
    path('Profile/', views.renderProfile),
    path('logout/',views.logout),
    
    
    path('manageUser/', views.manageUsers),
    path('editUserPage/<int:id>', views.manageUserForm),
    path('editUserValidate/<int:id>', views.editUserValidate),
    path('deleteUser/<int:id>', views.deleteUser),
    path('News/', views.renderNews), 
]
