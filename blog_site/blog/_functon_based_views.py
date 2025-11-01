from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .models import Post
from .forms import PostForm


def post_list(request: HttpRequest) -> HttpResponse:
    """
    Display a list of all blog posts, newest first.
    """
    posts = Post.objects.all()
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Display a single blog post by slug.
    """
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post_detail.html", {"post": post})


def post_create(request: HttpRequest) -> HttpResponse:
    """
    Create a new blog post.
    """
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})


def post_update(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Update an existing blog post.
    """
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_form.html", {"form": form, "post": post})


def post_delete(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Delete a blog post.
    """
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        return redirect("blog:post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})
