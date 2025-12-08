from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from sams import views as sams_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sams.urls')),
    # Custom logout that works with both GET and POST
    path('accounts/logout/', sams_views.custom_logout, name='logout'),
    # Use Django's built-in auth views for login and password management
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
