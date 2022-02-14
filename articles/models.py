from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    title = models.CharField('Название', max_length=20)
    full_text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации')
    is_private = models.BooleanField('Только для авторизированных', default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
