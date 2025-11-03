from django.urls import path
from .auth_views import (
    CustomLoginView, CustomLogoutView, UserRegistrationView,
    custom_login_view, custom_logout_view, register_view
)

app_name = 'auth'

urlpatterns = [
    # Class-based views (primary)
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    
    # Function-based alternatives (for flexibility)
    path('login-func/', custom_login_view, name='login_func'),
    path('logout-func/', custom_logout_view, name='logout_func'),
    path('register-func/', register_view, name='register_func'),
]