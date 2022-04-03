from django.urls import path
import system.domains.ManagePermissions.ManagePermissionsController as views


urlpatterns = [
    path('managePermissions/', views.managePermissions),
    path('deletePermission/<int:id>', views.deletePermission),
    path('CreatePermission/', views.createPermission),
    path('permissionValidate/', views.permissionValidate),
]