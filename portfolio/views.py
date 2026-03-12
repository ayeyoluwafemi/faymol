from django.shortcuts import render
from blog.models import Post  # Import the new database model


def index(request):
    # Fetch the 3 most recent published posts
    recent_posts = Post.objects.filter(
        is_published=True).order_by('-published_at')[:3]

    # Pass them to the template
    context = {
        'recent_posts': recent_posts
    }
    return render(request, 'portfolio/index.html', context)
