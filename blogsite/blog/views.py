from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Post


# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    # using the Django paginator - takes the list of objects and the number of objects per page
    paginator = Paginator(post_list, 5)  # 5 posts in each page
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post_slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})
