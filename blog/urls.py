from django.urls import path
from . import views

# Add an app_name, it makes linking much safer!
app_name = 'blog'

urlpatterns = [
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
