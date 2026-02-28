from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article


def article_list(request):
    articles = Article.objects.filter(status='published')
    tag_slug = request.GET.get('tag')
    if tag_slug:
        articles = articles.filter(tags__slug=tag_slug)
    paginator = Paginator(articles, 9)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'articles/article_list.html', {
        'articles': articles,
        'current_tag': tag_slug,
    })


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    return render(request, 'articles/article_detail.html', {'article': article})
