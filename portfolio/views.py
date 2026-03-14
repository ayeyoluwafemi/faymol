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

        # 1. Format the notification email sent to YOU
        admin_message = f"New message from: {name} ({sender_email})\n\n{message}"

        # 2. Format the auto-reply confirmation sent to the SENDER
        client_subject = "Message Received - Femi Ayeyemi"
        client_message = f"Hi {name},\n\nThank you for reaching out. This is an automated confirmation that I have received your message regarding '{subject}'.\n\nI will review your inquiry and get back to you shortly.\n\nBest regards,\n\nFemi Ayeyemi\nSoftware Engineer & QA Expert\nfemiayeyemi.com"

        try:
            # Send the notification to your inbox
            send_mail(
                subject=f"Website Inquiry: {subject}",
                message=admin_message,
                from_email='contact@femiayeyemi.com',
                recipient_list=['contact@femiayeyemi.com'],
                fail_silently=False,
            )

            # Send the confirmation auto-reply to the client
            send_mail(
                subject=client_subject,
                message=client_message,
                from_email='contact@femiayeyemi.com',
                recipient_list=[sender_email],
                fail_silently=False,
            )

            # Show success message on the website
            messages.success(
                request, "Your message has been sent successfully. I will be in touch soon!")
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
