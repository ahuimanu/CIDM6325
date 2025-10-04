from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Post
from django.utils import timezone


class PostList(ListView):
    queryset = Post.objects.filter(status="published")
    context_object_name = "posts"
    template_name = "blog/post_list.html"

class PostDetail(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields =  ["title", "body", "status", "published_at"]
    template_name = "blog/post_form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["published_at"] = timezone.now()
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        # auto-slug from title if empty
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        if form.instance.status == Post.PUBLISHED and not form.instance.published_at:
            form.instance.published_at = timezone.now()     
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "body", "status", "published_at"]
    template_name = "blog/post_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def form_valid(self, form):
        if form.instance.status == Post.PUBLISHED and not form.instance.published_at:
            form.instance.published_at = timezone.now()
        return super().form_valid(form)

class PostDelete(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"


# Create your views here.
