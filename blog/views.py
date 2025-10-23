from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .mixins import AuthorOrStaffRequiredMixin  # if you have this mixin

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
    fields = ["title", "body", "status"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# -------------------------------
# UPDATE VIEW
# -------------------------------
class PostUpdateView(LoginRequiredMixin, AuthorOrStaffRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "body", "status"]
    template_name = "blog/post_form.html"

# -------------------------------
# DELETE VIEW
# -------------------------------
class PostDeleteView(LoginRequiredMixin, AuthorOrStaffRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
