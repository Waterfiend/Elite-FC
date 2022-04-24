from django.urls import path
import system.domains.ManageUsers.ManageUsersController as views


urlpatterns = [
    path('manageUser/', views.manageUsers),# render all the users and their information in a table
    path('editUserPage/<int:id>', views.manageUserForm),# edit/create user form
    path('editUserValidate/<int:id>', views.editUserValidate),# validate user before commiting changes to database
    path('deleteUser/<int:id>', views.deleteUser),# delete a user based on id
]