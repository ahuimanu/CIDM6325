from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from .models import Post, Category
from .forms import PostForm, CommentForm

def post_list(request):
    q = request.GET.get('q', '')
    posts = Post.objects.filter(is_published=True)
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/post_list.html', {'posts': posts, 'q': q})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created.')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated.')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
@permission_required('blog.can_publish', raise_exception=True)
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.is_published = True
    post.save(update_fields=['is_published'])
    messages.success(request, 'Post published.')
    return redirect('blog:post_detail', pk=pk)

# HTMX live search endpoint
@require_http_methods(['GET'])
def post_search(request):
    q = request.GET.get('q', '')
    posts = Post.objects.filter(is_published=True)
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/_post_list_items.html', {'posts': posts})

@login_required
@require_http_methods(['POST'])
def comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        messages.success(request, 'Comment added.')
        return redirect('blog:post_detail', pk=pk)
    messages.error(request, 'Invalid comment.')
    return redirect('blog:post_detail', pk=pk)
