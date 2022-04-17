from django.urls import path
import system.domains.News.NewsController as views


urlpatterns = [
    path('News/', views.HomeView.as_view(), name = "news"),
    path('Newsfront/', views.HomeViewFront.as_view(), name  = "newsfront"),
    path('article/<int:pk>',views.ArticleDetailView.as_view(), name = 'article-detail'), #pk is the privatekey of each entry, each post  has its own unique primary key
    path('articledet/<int:pk>',views.ArticleDetailViewFront.as_view(), name = 'article-detailfront'),
    path('add_post/', views.AddPostView.as_view(), name = 'add_post'),
    path('article/edit/<int:pk>', views.UpdatePostView.as_view(), name = 'update_post'),
    path('article/<int:pk>/delete', views.DeletePostView.as_view(), name = 'delete_post'),
]