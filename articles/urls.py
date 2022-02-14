from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='articles'),
    path('articles/create/', views.ArticleCreateView.as_view()),
    path('articles/<int:pk>/update', views.ArticleUpdateView.as_view()),
    path('articles/<int:pk>/detail', views.ArticleDetailView.as_view()),
]
