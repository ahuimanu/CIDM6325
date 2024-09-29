import os

from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.views.generic import ListView
from .forms import EmailPostForm
from .models import Post


# Create your views here.
def post_list(request):
    """
    A view that returns a list of published posts
    """
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


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation - cleaned and sanitized data are essential
            cd = form.cleaned_data
            # ... send email - this should be separated into a service soon
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} {cd['email']} thinks you would like {post.title}"
            message = f"Hi, have a look at {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(
                subject=subject, 
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
            
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form
        }
    )




# CBV versions
# CBVs are a matter of taste and some find that they better structure and application
# by enforcing object orientation and separation of concerns
# https://docs.djangoproject.com/en/5.0/topics/class-based-views/intro/
class PostListView(ListView):
    """
    Alternative post list view
    """    
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 5 # 5 posts per page - CoPilot detected this, nicely done
    template_name = "blog/post/list.html"