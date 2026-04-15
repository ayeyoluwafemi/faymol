from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import urllib.request
import urllib.parse
import json
from .models import Project
from blog.models import Post
import time


def index(request):
    if request.method == 'POST':
        # 1. CLOUDFLARE TURNSTILE VERIFICATION
        turnstile_response = request.POST.get('cf-turnstile-response', '')
        data = urllib.parse.urlencode({
            'secret': settings.TURNSTILE_SECRET_KEY,
            'response': turnstile_response
        }).encode('utf-8')
        req = urllib.request.Request(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify', data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())

        if not result.get('success'):
            messages.error(request, "Security check failed. Please try again.")
            return redirect('/#contact')

        # 2. THE HONEYPOT TRAP
        # If this hidden field has ANY data, it's a bot blindly filling out the form.
        if request.POST.get('company_website'):
            # Fake success to fool the bot
            messages.success(
                request, "Your message has been sent successfully.")
            return redirect('/#contact')

        # 3. RATE LIMITING (Cooldown Timer)
        # Prevents the same user/bot from sending multiple emails in a 2-minute window
        last_submit = request.session.get('last_submit', 0)
        current_time = time.time()
        if current_time - last_submit < 120:
            # Fake success
            messages.success(
                request, "Your message has been sent successfully.")
            return redirect('/#contact')

        # 4. KEYWORD FILTER (The Bouncer)
        message = request.POST.get('message', '')
        spam_keywords = ['http://', 'https://', 'crypto',
                         'seo', 'marketing', 'investment', 'bitcoin']
        if any(keyword in message.lower() for keyword in spam_keywords):
            # Fake success
            messages.success(
                request, "Your message has been sent successfully.")
            return redirect('/#contact')

        # --- IF IT PASSES ALL TRAPS, SEND THE EMAIL ---

        # Start the cooldown timer
        request.session['last_submit'] = current_time

        name = request.POST.get('name')
        sender_email = request.POST.get('email')
        subject = request.POST.get('subject')

        admin_message = f"New message from: {name} ({sender_email})\n\n{message}"
        client_subject = "Message Received - Femi Ayeyemi"
        client_message = f"Hi {name},\n\nThank you for reaching out. This is an automated confirmation that I have received your message regarding '{subject}'.\n\nI will review your inquiry and get back to you shortly.\n\nBest regards,\n\nFemi Ayeyemi\nSoftware Engineer & QA Expert\nfemiayeyemi.com"

        try:
            send_mail(
                subject=f"Website Inquiry: {subject}",
                message=admin_message,
                from_email='contact@femiayeyemi.com',
                recipient_list=['contact@femiayeyemi.com'],
                fail_silently=False,
            )

            send_mail(
                subject=client_subject,
                message=client_message,
                from_email='contact@femiayeyemi.com',
                recipient_list=[sender_email],
                fail_silently=False,
            )

            messages.success(
                request, "Your message has been sent successfully. I will be in touch soon!")
            return redirect('/#contact')

        except Exception as e:
            messages.error(
                request, "There was an error sending your message. Please try again.")
            return redirect('/#contact')
