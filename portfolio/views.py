from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Project
from blog.models import Post


def index(request):
    # --- Handle the Contact Form Submission ---
    if request.method == 'POST':
        name = request.POST.get('name')
        sender_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Format how the email will look in your inbox
        full_message = f"New message from: {name} ({sender_email})\n\n{message}"

        try:
            send_mail(
                subject=f"Website Inquiry: {subject}",
                message=full_message,
                # Ensure this matches your sending config later
                from_email='contact@femiayeyemi.com',
                # Where you want to receive it
                recipient_list=['contact@femiayeyemi.com'],
                fail_silently=False,
            )
            # Send a success message back to the template
            messages.success(
                request, "Your message has been sent successfully. I will be in touch soon!")
            # Refresh the page and jump back to the form
            return redirect('/#contact')
        except Exception as e:
            messages.error(
                request, "There was an error sending your message. Please try again.")
            return redirect('/#contact')

    # --- Fetch Database Content ---
    featured_projects = Project.objects.all()
    recent_posts = Post.objects.filter(
        is_published=True).order_by('-published_at')[:3]

    context = {
        'featured_projects': featured_projects,
        'recent_posts': recent_posts,
    }

    return render(request, 'portfolio/index.html', context)
