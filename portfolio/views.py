from django.shortcuts import render
# Import the Project model from the current (portfolio) app
from .models import Project
from blog.models import Post  # Your existing blog import

# If you also created a Testimonial model, you can import it like this:
# from .models import Project, Testimonial


def index(request):
    # 1. Fetch the projects
    # We are grabbing all projects here. If you added an 'is_published' or 'is_featured'
    # field to your Project model, you can filter it just like you did with posts!
    featured_projects = Project.objects.all()

    # 2. Fetch the 3 most recent published posts
    recent_posts = Post.objects.filter(
        is_published=True).order_by('-published_at')[:3]

    # 3. Fetch testimonials (Uncomment if you have this model set up in your database)
    # testimonials = Testimonial.objects.all()

    # Pass everything to the template
    context = {
        'featured_projects': featured_projects,
        'recent_posts': recent_posts,
        # 'testimonials': testimonials,
    }

    return render(request, 'portfolio/index.html', context)
