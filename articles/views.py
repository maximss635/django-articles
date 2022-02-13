from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, TemplateView, CreateView
from django.views.generic.edit import ProcessFormView

from .forms import ArticleForm
from .models import Article
from datetime import datetime


def index(request):
    articles = Article.objects.order_by('date')
    if not request.user.is_authenticated:
        articles = articles.filter(is_private=False)

    context = {}
    if len(articles) > 0:
        context['articles'] = articles

    return render(request, 'articles/index.html', context)


class ArticleCreateView(CreateView):
    template_name = 'articles/create.html'
    model = Article
    form_class = ArticleForm
    extra_context = {'title': 'Создание статьи'}

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('create')

        current_date = str(datetime.now())
        article = self.model(author=request.user, date=current_date)
        form = self.form_class(request.POST, instance=article)

        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'articles/create.html', {
                'form': self.form_class(),
                'error': 'Некорректно заполнены формы',
            })


class ArticleDeleteView(TemplateView):
    model = Article
    context_object_name = 'article'
    object = None

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.model.objects.get(id=kwargs['pk'])
        except Article.DoesNotExist:
            return HttpResponseNotFound("<h1>Page not found</h1>")

        if request.user.is_superuser or self.object.author == request.user:
            self.object.delete()
            return redirect('index')
        else:
            request.session['article_error'] = 'Вы можете удалять только свои статьи'
            return redirect('/articles/{}'.format(kwargs['pk']))


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'articles/create.html'
    form_class = ArticleForm
    context_object_name = 'article'
    object = None
    extra_context = {'title': 'Редактирование статьи'}

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.model.objects.get(id=kwargs['pk'])
        except self.model.DoesNotExist:
            return HttpResponseNotFound("<h1>Page not found</h1>")

        if request.user != self.object.author:
            request.session['article_error'] = 'Вы можете редактировать только свои статьи'
            return redirect('/articles/{}'.format(kwargs['pk']))
        else:
            return ProcessFormView.get(self, request, args, kwargs)


class ArticleDetailView(TemplateView):
    model = Article
    template_name = 'articles/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        try:
            article = self.model.objects.get(id=kwargs['pk'])
        except self.model.DoesNotExist:
            return HttpResponseNotFound("<h1>Page not found</h1>")

        if not request.user.is_authenticated and article.is_private:
            return HttpResponseNotFound("<h1>Page not found</h1>")

        try:
            error = request.session['article_error']
            request.session['article_error'] = ''
        except KeyError:
            error = ''

        return render(request, self.template_name, {
            self.context_object_name: article,
            'error': error
        })
