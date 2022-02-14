from rest_framework import permissions, generics

from .models import Article
from .serializers import ArticleSerializer
from .permissions import IsOwnerOrAdmin, IsPublicArticle
from .filters import PrivateArticleFilter


# /
class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filter_backends = [PrivateArticleFilter]


# /articles/<int:pk>/detail
class ArticleDetailView(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsPublicArticle]


# /articles/<int:pk>/update
class ArticleUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsOwnerOrAdmin]


# /articles/create/
class ArticleCreateView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
