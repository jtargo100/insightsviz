from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import BlogPost


def post_list(request):
    posts = BlogPost.objects.filter(status='published')
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'current_tag': tag_slug,
    })


def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    return render(request, 'blog/post_detail.html', {'post': post})
