from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Comment
from .forms import CommentForm


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)

    # Only fetch top-level comments (replies will be fetched in the template)
    comments = post.comments.filter(active=True, parent__isnull=True)

    if request.method == 'POST':
        # HONEYPOT TRAP: If bots fill this hidden field, silently drop the comment
        if request.POST.get('website_url'):
            messages.success(request, "Your comment has been posted!")
            return redirect('blog:post_detail', slug=post.slug)

        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post

            # Check if this is a reply to another comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                new_comment.parent = Comment.objects.get(id=parent_id)

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

# NEW: Function to handle likes via JavaScript fetch


def like_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)

        # Use sessions to prevent a user from liking the same comment 100 times
        liked_comments = request.session.get('liked_comments', [])
        if comment_id not in liked_comments:
            comment.likes += 1
            comment.save()
            liked_comments.append(comment_id)
            request.session['liked_comments'] = liked_comments
            return JsonResponse({'success': True, 'likes': comment.likes})

        return JsonResponse({'success': False, 'error': 'Already liked'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
