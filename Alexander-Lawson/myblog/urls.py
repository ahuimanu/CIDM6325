from django.urls import path
from . import views

urlpatterns = [
    # ...existing code...
    path('blog/', views.blog_list, name='blog_list'),
]