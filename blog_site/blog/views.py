from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    """
    Display a list of all blog posts, newest first.
    """

    model = Post
    context_object_name = "posts"
    template_name = "blog/post_list.html"

    def get_queryset(self):
        """
        Only show posts with publish_date <= now (published).
        """
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by(
            "-publish_date"
        )


class PostDetailView(DetailView):
    """
    Display a single blog post by slug.
    """

    model = Post
    template_name = "blog/post_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        """
        Only allow access to published posts.
        """
        return Post.objects.filter(publish_date__lte=timezone.now())


class PostCreateView(CreateView):
    """
    Create a new blog post.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={"slug": self.object.slug})


class PostUpdateView(UpdateView):
    """
    Update an existing blog post.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={"slug": self.object.slug})


class PostDeleteView(DeleteView):
    """
    Delete a blog post.
    """

    model = Post
    template_name = "blog/post_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("blog:post_list")
