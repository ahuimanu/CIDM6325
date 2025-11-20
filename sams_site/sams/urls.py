from django.urls import path
from . import views

app_name = 'sams'

urlpatterns = [
    # Calendar as main page
    path('', views.CalendarView.as_view(), name='calendar'),
    
    # Calendar events
    path('events/add/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    
    # Blog/Announcements
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:announcement_id>/comment/', views.comment_create, name='comment_create'),
    
    # Items (secondary feature)
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/new/', views.ItemCreateView.as_view(), name='item_create'),
    path('items/<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item_edit'),
    path('items/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    
    # Authentication
    path('accounts/register/', views.register, name='register'),
]
