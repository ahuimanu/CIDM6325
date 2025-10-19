
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView

app_name = 'blog'


from .views import PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('index/', PostListView.as_view(), name='index'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]