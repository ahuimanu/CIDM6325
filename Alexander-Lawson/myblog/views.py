from django.shortcuts import render
from .models import BlogPost  # Assuming a BlogPost model exists

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-published_date')  # Fetch posts ordered by date
    return render(request, 'myblog/blog_list.html', {'posts': posts})