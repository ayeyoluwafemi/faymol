from django.urls import path
from . import views

# Add an app_name, it makes linking much safer!
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('comment/<int:comment_id>/like/',
         views.like_comment, name='like_comment'),
]
