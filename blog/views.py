from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .mixins import AuthorOrStaffRequiredMixin


# -------------------------------
# LIST VIEW (with pagination)
# -------------------------------
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 2  # TEMPORARY so you can see Prev/Next

    def get_queryset(self):
        now = timezone.now()
        return (
            Post.objects
                .filter(status=Post.PUBLISHED, published_at__lte=now)
                .order_by("-published_at", "-created_at")
        )

# -------------------------------
# DETAIL VIEW
# -------------------------------
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

# -------------------------------
# CREATE VIEW
# -------------------------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "body", "status", "image"]
    template_name = "blog/post_form.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# ------------------------------
# UPDATE VIEW
# ------------------------------
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "body", "status", "image"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # prevent someone from changing author in the form
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return (
            post.author == self.request.user
            or self.request.user.is_staff
            or self.request.user.is_superuser
        )


# ------------------------------
# DELETE VIEW
# ------------------------------
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")

    def test_func(self):
        post = self.get_object()
        return (
            post.author == self.request.user
            or self.request.user.is_staff
            or self.request.user.is_superuser
        )
