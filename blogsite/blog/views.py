from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Post


# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    # using the Django paginator - takes the list of objects and the number of objects per page
    paginator = Paginator(post_list, 5)  # 5 posts in each page

    # test for and handle page out of bounds errors
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    # what if the page requested is not a number?
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    # what if the page requested is out of range?
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)

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
