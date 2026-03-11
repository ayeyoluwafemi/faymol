from django.contrib import admin
from .models import Project, Testimonial


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    # Automatically fills the slug based on the title
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_role', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('client_name', 'feedback')
