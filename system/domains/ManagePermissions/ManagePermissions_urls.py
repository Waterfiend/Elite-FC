from django.urls import path
import system.domains.ManagePermissions.ManagePermissionsController as views


urlpatterns = [
    path('managePermissions/', views.managePermissions),# display the permissions page
    path('deletePermission/<int:id>', views.deletePermission),# delete a permission by id
    path('CreatePermission/', views.createPermission),# displays the creat permission form
    path('permissionValidate/', views.permissionValidate),# validate the permission before commiting it to the database
]