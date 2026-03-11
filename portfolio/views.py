from django.shortcuts import render
from .models import Project, Testimonial


def home(request):
    # Fetch all projects, ordered by the newest first (based on model Meta)
    projects = Project.objects.all()
    # Fetch only active testimonials
    testimonials = Testimonial.objects.filter(is_active=True)

    context = {
        'projects': projects,
        'testimonials': testimonials,
    }
    return render(request, 'portfolio/index.html', context)
