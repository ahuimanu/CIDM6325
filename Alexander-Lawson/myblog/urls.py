from django.urls import path
from .views import BlogPostDetailView

app_name = 'blog'

urlpatterns = [
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'),
]