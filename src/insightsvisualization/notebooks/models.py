from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class NotebookVisualization(models.Model):
    """Jupyter notebook rendered as an interactive visualization."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notebooks',
    )
    description = models.TextField(max_length=500, blank=True)
    notebook_file = models.FileField(
        upload_to='notebooks/files/%Y/%m/',
        help_text='Upload a .ipynb Jupyter Notebook file.',
    )
    rendered_html = models.TextField(
        blank=True,
        help_text='Auto-generated HTML from the notebook.',
    )
    featured_image = models.ImageField(
        upload_to='notebooks/images/%Y/%m/',
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        'core.Tag',
        blank=True,
        related_name='notebooks',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Notebook Visualization'
        verbose_name_plural = 'Notebook Visualizations'
        indexes = [
            models.Index(fields=['-published_date']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('notebooks:notebook_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    """User comments on notebook visualizations."""
    notebook = models.ForeignKey(
        NotebookVisualization,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notebook_comments',
    )
    body = models.TextField(max_length=2000)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_date']
        indexes = [
            models.Index(fields=['created_date']),
        ]

    def __str__(self):
        return f'Comment by {self.author.username} on {self.notebook.title}'
