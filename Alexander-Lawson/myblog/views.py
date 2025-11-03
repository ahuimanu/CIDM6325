from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for blog posts - requires authentication
    Only authenticated users can create posts
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:index')
    login_url = '/auth/login/'
    
    def get_form_kwargs(self):
        """Pass user to form"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        print("[DEBUG] PostCreateView: form_valid called. Data:", form.cleaned_data)
        # Set the author to the current user
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        print("[DEBUG] PostCreateView: form_invalid called. Errors:", form.errors)
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update view for blog posts - requires authentication and ownership
    Only the author of the post or staff members can edit posts
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    login_url = '/auth/login/'
    
    def get_form_kwargs(self):
        """Pass user to form"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def test_func(self):
        """
        Test if user can edit this post
        Authors can edit their own posts, staff can edit any post
        """
        post = self.get_object()
        return (
            self.request.user == post.author or 
            self.request.user.is_staff or 
            self.request.user.is_superuser
        )
    
    def handle_no_permission(self):
        """
        Custom handling for permission denied
        """
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Please log in to edit posts.')
            return redirect('auth:login')
        else:
            messages.error(self.request, 'You can only edit your own posts.')
            return redirect('blog:post_detail', pk=self.get_object().pk)
    
    def form_valid(self, form):
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)



# CBV for deleting a blog post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete view for blog posts - requires authentication and ownership
    Only the author of the post or staff members can delete posts
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:post_list')
    login_url = '/auth/login/'
    
    def test_func(self):
        """
        Test if user can delete this post
        Authors can delete their own posts, staff can delete any post
        """
        post = self.get_object()
        return (
            self.request.user == post.author or 
            self.request.user.is_staff or 
            self.request.user.is_superuser
        )
    
    def handle_no_permission(self):
        """
        Custom handling for permission denied
        """
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Please log in to delete posts.')
            return redirect('auth:login')
        else:
            messages.error(self.request, 'You can only delete your own posts.')
            return redirect('blog:post_detail', pk=self.get_object().pk)
    
    def delete(self, request, *args, **kwargs):
        """
        Override delete to add success message
        """
        messages.success(request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
