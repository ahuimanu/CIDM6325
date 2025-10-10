from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_details_view, name='home_details'),  # Set as default view
    path('home-details/', views.home_details_view, name='home_details'),
    path('home-details-list/', views.home_details_list_view, name='home_details_list'),
]