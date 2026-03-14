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
