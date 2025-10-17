from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.contrib import messages

from .models import Post
from .forms import PostForm, CommentForm

class HtmxQueryMixin:
    """Adds simple 'q' filtering to ListView."""
    q_param = 'q'
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get(self.q_param, '')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(body__icontains=q))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get(self.q_param, '')
        return ctx

class PostListView(HtmxQueryMixin, generic.ListView):
    model = Post
    queryset = Post.objects.filter(is_published=True)
    context_object_name = "posts"
    template_name = "blog/post_list.html"

class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = CommentForm()
        return ctx

class AuthorRequiredMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created.')
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={'pk': self.object.pk})

class PostUpdateView(AuthorRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    def form_valid(self, form):
        messages.success(self.request, 'Post updated.')
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={'pk': self.object.pk})

class PostDeleteView(AuthorRequiredMixin, generic.DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted.')
        return super().delete(request, *args, **kwargs)

class PostPublishView(PermissionRequiredMixin, generic.View):
    permission_required = "blog.can_publish"
    raise_exception = True
    def post(self, request, pk):
        post = Post.objects.get(pk=pk, author=request.user)
        post.is_published = True
        post.save(update_fields=['is_published'])
        messages.success(request, 'Post published.')
        return redirect("blog:post_detail", pk=pk)

class CommentCreateView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.author = request.user
            c.post = post
            c.save()
            messages.success(request, 'Comment added.')
        else:
            messages.error(request, 'Invalid comment.')
        return redirect("blog:post_detail", pk=pk)
