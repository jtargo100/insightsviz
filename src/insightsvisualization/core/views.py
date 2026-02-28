from django.shortcuts import render
from insightsvisualization.blog.models import BlogPost
from insightsvisualization.articles.models import Article
from insightsvisualization.notebooks.models import NotebookVisualization


def home(request):
    """Landing page with featured content."""
    latest_posts = BlogPost.objects.filter(status='published')[:3]
    latest_articles = Article.objects.filter(status='published')[:3]
    latest_notebooks = NotebookVisualization.objects.filter(status='published')[:3]
    return render(request, 'core/home.html', {
        'latest_posts': latest_posts,
        'latest_articles': latest_articles,
        'latest_notebooks': latest_notebooks,
    })


def about(request):
    return render(request, 'core/about.html')
