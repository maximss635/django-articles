from django.forms import ModelForm, TextInput, Textarea
from .models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'date']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            'full_text': Textarea(attrs={
                'placeholder': 'Текст статьи',
                'class': 'form-control'
            })
        }
