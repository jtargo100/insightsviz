from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NotebookVisualization, Comment
from .forms import CommentForm


def notebook_list(request):
    notebooks = NotebookVisualization.objects.filter(status='published')
    tag_slug = request.GET.get('tag')
    if tag_slug:
        notebooks = notebooks.filter(tags__slug=tag_slug)
    paginator = Paginator(notebooks, 9)
    page = request.GET.get('page')
    notebooks = paginator.get_page(page)
    return render(request, 'notebooks/notebook_list.html', {
        'notebooks': notebooks,
        'current_tag': tag_slug,
    })


def notebook_detail(request, slug):
    notebook = get_object_or_404(
        NotebookVisualization, slug=slug, status='published'
    )
    comments = notebook.comments.filter(is_approved=True)
    comment_form = CommentForm()
    return render(request, 'notebooks/notebook_detail.html', {
        'notebook': notebook,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def add_comment(request, slug):
    notebook = get_object_or_404(
        NotebookVisualization, slug=slug, status='published'
    )
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.notebook = notebook
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted.')
        else:
            messages.error(request, 'There was an error with your comment.')
    return redirect('notebooks:notebook_detail', slug=slug)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user or request.user.is_staff:
        slug = comment.notebook.slug
        comment.delete()
        messages.success(request, 'Comment deleted.')
        return redirect('notebooks:notebook_detail', slug=slug)
    messages.error(request, 'You cannot delete this comment.')
    return redirect('notebooks:notebook_list')
