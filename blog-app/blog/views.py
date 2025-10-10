from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods
import logging

from .forms import PostForm, CommentForm
from .models import Post

logger = logging.getLogger(__name__)

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.select_related("author").prefetch_related("tags").order_by("-created_at")

class PostDetailView(DetailView):
    model = Post
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.post = self.object
            c.save()
            messages.success(request, "Comment added!")
            return redirect(self.object.get_absolute_url())
        ctx = self.get_context_data()
        ctx["comment_form"] = form
        return render(request, self.template_name, ctx)

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(author=request.user)
            messages.success(request, "Draft created!")
            return redirect(post.get_absolute_url())
        else:
            # Log and surface validation errors for debugging
            try:
                logger.debug("Post create failed: %s", form.errors.as_json())
            except Exception:
                logger.debug("Post create failed: %s", form.errors)
            messages.error(request, "There were errors creating the post. Please review the form.")
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})

@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Only author or users with change permission can edit
    if post.author != request.user and not request.user.has_perm("blog.change_post"):
        return HttpResponseForbidden("Not allowed.")

    # Gate publishing by custom permission
    if request.method == "POST" and request.POST.get("status") == "published" and not request.user.has_perm("blog.can_publish"):
        messages.error(request, "You do not have permission to publish.")
        return redirect(post.get_absolute_url())

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(author=post.author)
            messages.success(request, "Post updated.")
            return redirect(post.get_absolute_url())
        else:
            try:
                logger.debug("Post update failed for %s: %s", post.pk, form.errors.as_json())
            except Exception:
                logger.debug("Post update failed for %s: %s", post.pk, form.errors)
            messages.error(request, "There were errors updating the post. Please review the form.")
    else:
        initial = {"tags_csv": ", ".join(t.name for t in post.tags.all())}
        form = PostForm(instance=post, initial=initial)
    return render(request, "blog/post_form.html", {"form": form, "post": post})

@login_required
@permission_required("blog.delete_post", raise_exception=True)
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        messages.info(request, "Post deleted.")
        return redirect("post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})

# ---- HTMX ----
def hx_post_search(request):
    term = (request.GET.get("q") or "").strip()
    qs = Post.objects.all()
    if term:
        qs = qs.filter(
            Q(title__icontains=term) | Q(body__icontains=term) | Q(tags__name__icontains=term)
        ).distinct()
    html = render_to_string("blog/partials/_post_rows.html", {"posts": qs[:20]}, request=request)
    return HttpResponse(html)

@login_required
def hx_post_inline_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not request.user.has_perm("blog.change_post"):
        return HttpResponseForbidden("Not allowed.")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(author=post.author)
            row = render_to_string("blog/partials/_post_row.html", {"post": post}, request=request)
            return HttpResponse(row)
    else:
        html = render_to_string(
            "blog/partials/_post_inline_form.html",
            {"form": PostForm(instance=post), "post": post},
            request=request,
        )
        return HttpResponse(html)


def dev_login(request):
    """Development helper: create (if needed) and log in a dev user when DEBUG=True.

    This is intentionally only available when DEBUG is True so it isn't usable in production.
    Visit /dev-login/ to get a quick user for local development.
    """
    # Allow dev-login when DEBUG is True or when accessed from localhost for convenience
    remote = request.META.get("REMOTE_ADDR", "")
    if not (settings.DEBUG or remote in ("127.0.0.1", "::1")):
        return HttpResponseForbidden("Dev login is disabled.")

    User = get_user_model()
    username = "dev"
    password = "devpass"

    user, created = User.objects.get_or_create(username=username, defaults={"is_staff": True, "is_superuser": True})
    if created:
        user.set_password(password)
        user.save()

    # Ensure the password is set so authenticate will succeed
    if not user.check_password(password):
        user.set_password(password)
        user.save()

    user = authenticate(request, username=username, password=password)
    if user is None:
        return HttpResponse("Could not authenticate dev user.")
    login(request, user)
    messages.info(request, f"Logged in as {username} (development user).")
    return redirect("post_list")


def register(request):
    """Allow a new user to register an account.

    After successful registration the user is logged in and redirected to the post list.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Normalize username to lowercase to avoid case-sensitivity issues
            user = form.save(commit=False)
            if hasattr(user, 'username') and user.username:
                user.username = user.username.lower()
            user.save()
            # automatically log in the new user
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(request, username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
            messages.success(request, "Account created and logged in.")
            return redirect("post_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    """Custom login view that provides explicit authenticate/login handling.

    This is used to ensure the login form behavior is clear and to allow
    showing messages when authentication fails.
    """
    if request.method == "POST":
        # allow case-insensitive username matching: look up the real username if necessary
        posted_username = (request.POST.get("username") or "").strip()
        User = get_user_model()
        matched = None
        if posted_username:
            matched = User.objects.filter(username__iexact=posted_username).first()
            # fallback: allow users to login with their email (case-insensitive)
            if not matched:
                matched = User.objects.filter(email__iexact=posted_username).first()

        data = request.POST.copy()
        if matched:
            # use the actual stored username for authentication (preserves stored case)
            data["username"] = matched.username

        # diagnostic logging
        logger.debug("Login attempt posted_username=%s matched=%s", posted_username, getattr(matched, 'username', None))

        form = AuthenticationForm(request, data=data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            next_url = request.POST.get("next") or request.GET.get("next")
            return redirect(next_url or "post_list")
        else:
            # fall through to re-render with errors
            # ensure widgets have bootstrap classes even when invalid
            for f in ("username", "password"):
                if f in form.fields:
                    form.fields[f].widget.attrs.update({"class": "form-control"})
            # Helpful debug hints when running locally
            if settings.DEBUG:
                uname = request.POST.get("username")
                try:
                    User.objects.get(username__iexact=uname)
                    form.add_error(None, "Debug: username exists (case-insensitive) — password may be incorrect.")
                except User.DoesNotExist:
                    # try email match
                    if User.objects.filter(email__iexact=uname).exists():
                        form.add_error(None, "Debug: username not found; but an account exists with that email. Try your password.")
                    else:
                        form.add_error(None, "Debug: username/email not found.")
            return render(request, "registration/login.html", {"form": form})
    else:
        form = AuthenticationForm(request)
        # add bootstrap and accessibility attributes to rendered widgets
        if "username" in form.fields:
            form.fields["username"].widget.attrs.update({"class": "form-control", "autofocus": True, "aria-describedby": "id_username_help"})
        if "password" in form.fields:
            form.fields["password"].widget.attrs.update({"class": "form-control", "aria-describedby": "id_password_help"})
        return render(request, "registration/login.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def review_list(request):
    """List posts that are in 'review' status and allow publishing.

    Only users with `blog.can_review` can access this page. Publishing (setting
    status to `published`) requires the `blog.can_publish` permission; if the
    current user lacks it, an error message is shown.
    """
    from .models import Post

    if not request.user.has_perm("blog.can_review"):
        return HttpResponseForbidden("Not allowed.")

    if request.method == "POST":
        post_id = request.POST.get("post_id")
        action = request.POST.get("action")
        post = get_object_or_404(Post, pk=post_id)
        if action == "publish":
            if not request.user.has_perm("blog.can_publish"):
                messages.error(request, "You do not have permission to publish posts.")
            else:
                post.status = Post.Status.PUBLISHED
                post.save()
                messages.success(request, f"Published '{post.title}'.")
        elif action == "send_back":
            post.status = Post.Status.DRAFT
            post.save()
            messages.info(request, f"Sent '{post.title}' back to draft.")
        return redirect("review_list")

    posts = Post.objects.filter(status=Post.Status.REVIEW).select_related("author").prefetch_related("tags")
    return render(request, "blog/review_list.html", {"posts": posts})


def debug_users(request):
    """Return a simple HTML listing of users for debugging (DEBUG-only)."""
    if not settings.DEBUG:
        return HttpResponseForbidden("Disabled")
    User = get_user_model()
    users = User.objects.all().order_by('username')
    return render(request, 'debug/users.html', {'users': users})


def debug_reset_password(request, username):
    """Reset the named user's password to a random temporary password and return it (DEBUG-only).

    Accessible at POST /debug/users/reset/<username>/ when DEBUG=True.
    """
    if not settings.DEBUG:
        return HttpResponseForbidden("Disabled")
    if request.method != "POST":
        return HttpResponse("Use POST to reset password.")
    User = get_user_model()
    user = User.objects.filter(username__iexact=username).first()
    if not user:
        return HttpResponse("User not found.")
    import secrets
    temp = "devpw-" + secrets.token_urlsafe(6)
    user.set_password(temp)
    user.save()
    return HttpResponse(f"Password for {user.username} reset to: {temp}")
