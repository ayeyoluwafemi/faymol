from django.shortcuts import render

# Create your views here.


def post_detail(request, slug):
    # This securely fetches the post or returns a standard 404 page if not found
    post = get_object_or_404(Post, slug=slug, is_published=True)

    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)
