from django.urls import path
import system.domains.ManageUsers.ManageUsersController as views


urlpatterns = [
    path('manageUser/', views.manageUsers),
    path('editUserPage/<int:id>', views.manageUserForm),
    path('editUserValidate/<int:id>', views.editUserValidate),
    path('deleteUser/<int:id>', views.deleteUser),
]