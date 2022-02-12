from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('articles/create', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/update', views.ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<int:pk>/delete', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('articles/<int:pk>', views.ArticleDetailView.as_view(), name='article_detail'),
]
