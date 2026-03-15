from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-published_at')
    context = {'posts': posts}
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)

    # Fetch all active comments for this specific post
    comments = post.comments.filter(active=True)

    # Handle the comment form submission
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post  # Link the comment to the current post
            new_comment.save()
            messages.success(request, "Your comment has been posted!")
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog/post_detail.html', context)
