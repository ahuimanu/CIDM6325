from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from .models import Post
from .forms import PostForm

# Create your views here.

class BlogPostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_view.html'
    context_object_name = 'post'


def post_list(request):
    """Function-based view to display all blog posts"""
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)


def post_create(request):
    """Function-based view to create a new blog post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    context = {
        'form': form
    }
    return render(request, 'blog/post_form.html', context)


def post_update(request, pk):
    """Function-based view to update an existing blog post"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'blog/post_form.html', context)


def post_delete(request, pk):
    """Function-based view to delete a blog post"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    
    context = {
        'post': post
    }
    return render(request, 'blog/post_confirm_delete.html', context)
