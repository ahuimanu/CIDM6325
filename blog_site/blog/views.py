from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PostForm
from .models import Post


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
        return Post.objects.published().order_by("-publish_date")


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
        return Post.objects.published()


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


class SearchView(ListView):
    """Simple full-text search over Post title/body with pagination.

    Query param `q` filters published posts via icontains on title/body.
    """

    model = Post
    context_object_name = "results"
    template_name = "blog/search_results.html"
    paginate_by = 10

    def get_queryset(self):
        q = (self.request.GET.get("q") or "").strip()
        base_qs = Post.objects.published()
        if not q:
            return base_qs.none()
        return base_qs.filter(Q(title__icontains=q) | Q(body__icontains=q))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = (self.request.GET.get("q") or "").strip()
        ctx["query"] = q
        ctx["count"] = self.get_queryset().count() if q else 0
        return ctx
