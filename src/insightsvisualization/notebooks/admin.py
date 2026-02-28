from django.contrib import admin
from .models import NotebookVisualization, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author', 'created_date']


@admin.register(NotebookVisualization)
class NotebookVisualizationAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'published_date']
    list_filter = ['status', 'published_date', 'tags']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ['-published_date']
    filter_horizontal = ['tags']
    raw_id_fields = ['author']
    inlines = [CommentInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'description', 'status'),
        }),
        ('Notebook', {
            'fields': ('notebook_file', 'rendered_html'),
        }),
        ('Media & Tags', {
            'fields': ('featured_image', 'tags'),
        }),
        ('Dates', {
            'fields': ('published_date',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-render notebook HTML when a notebook file is uploaded."""
        super().save_model(request, obj, form, change)
        if obj.notebook_file:
            try:
                from .utils import render_notebook
                obj.rendered_html = render_notebook(obj.notebook_file.path)
                obj.save(update_fields=['rendered_html'])
            except Exception:
                pass  # Silently fail if nbconvert is not available


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'notebook', 'created_date', 'is_approved']
    list_filter = ['is_approved', 'created_date']
    search_fields = ['body', 'author__username']
    actions = ['approve_comments', 'reject_comments']

    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Reject selected comments')
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
