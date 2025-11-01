
# logistics_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



# need to update this to use CBVs for orders instead of FBVs

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('logistics_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ Add this line
  
]
# logistics_project/urls.py
# Serve uploaded files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)