from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'published_at')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}  # Auto-fills the slug field
    date_hierarchy = 'published_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'author',
                    'is_approved', 'created_at', 'active')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author', 'content')
    date_hierarchy = 'created_at'
