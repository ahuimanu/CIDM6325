from django.shortcuts import render
from .models import BlogPost

def blog_list(request):
    posts = BlogPost.objects.all().order_by("-published_date")  # Double quotes used here
    return render(request, "myblog/blog_list.html", {"posts": posts})  # Double quotes used here