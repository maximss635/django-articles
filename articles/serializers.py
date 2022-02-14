from rest_framework import serializers
from .models import Article
from datetime import datetime


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date = serializers.HiddenField(default=datetime.now().__str__())

    class Meta:
        model = Article
        fields = ['title', 'full_text', 'id', 'is_private', 'date', 'author']
