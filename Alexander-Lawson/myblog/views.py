from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'author', 'content']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:index')

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'author', 'content']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')



# CBV for deleting a blog post
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:post_list')
