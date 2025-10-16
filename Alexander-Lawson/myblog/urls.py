from django.urls import path
from .views import BlogPostDetailView, post_list, post_create, post_update, post_delete

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'),
    path('post/create/', post_create, name='post_create'),
    path('post/<int:pk>/edit/', post_update, name='post_update'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
]