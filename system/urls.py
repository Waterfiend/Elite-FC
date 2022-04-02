from django.urls import path
import system.views as views

urlpatterns = [
    path('', views.hello),
    path('register/', views.renderRegistration),
    path('login', views.renderLogin),
    path('registerValidate/', views.validateRegistration),
    path('loginValidate/', views.validateLogin),
    path('News/', views.HomeView.as_view(), name = "news"),
    path('article/<int:pk>',views.ArticleDetailView.as_view(), name = 'article-detail'), #pk is the privatekey of each entry, each post  has its own unique primary key
    path('add_post/', views.AddPostView.as_view(), name = 'add_post'),
    path('article/edit/<int:pk>', views.UpdatePostView.as_view(), name = 'update_post'),
    path('article/<int:pk>/delete', views.DeletePostView.as_view(), name = 'delete_post'),
    path('Profile/', views.renderProfile),
    path('logout/', views.logout),

    path('manageUser/', views.manageUsers),
    path('editUserPage/<int:id>', views.manageUserForm),
    path('editUserValidate/<int:id>', views.editUserValidate),
    path('deleteUser/<int:id>', views.deleteUser),
    path('schedule/', views.display_schedule),
]
