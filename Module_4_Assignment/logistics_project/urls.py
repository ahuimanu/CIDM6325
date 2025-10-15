
# logistics_project/urls.py
from django.contrib import admin
from django.urls import path, include



# need to update this to use CBVs for orders instead of FBVs

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('logistics_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ Add this line
  
]
# logistics_project/urls.py