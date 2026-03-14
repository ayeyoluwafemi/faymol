from django.shortcuts import render

# Create your views here.


def post_detail(request, slug):
    # This securely fetches the post or returns a standard 404 page if not found
    post = get_object_or_404(Post, slug=slug, is_published=True)

    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)


def post_list(request):
    # Fetch ALL published posts, ordered by newest first
    posts = Post.objects.filter(is_published=True).order_by('-published_at')

    context = {
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)
