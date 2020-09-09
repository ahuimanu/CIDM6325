from django.urls import path, include
# from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),    
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register')
]
