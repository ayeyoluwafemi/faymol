from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')

    # UPGRADED: This gives you the WordPress-like editor with image uploads
    content = RichTextUploadingField()

    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(default=timezone.now)

    # UPGRADED: This adds the tagging system
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-published_at']  # Shows newest posts first

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.name}'
