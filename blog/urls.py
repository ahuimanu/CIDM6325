from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('search/', views.post_search, name='post_search'),  # HTMX endpoint
    path('comment/<int:pk>/add/', views.comment_add, name='comment_add'),
]
