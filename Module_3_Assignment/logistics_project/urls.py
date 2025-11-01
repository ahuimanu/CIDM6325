"""
URL configuration for logistics_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# logistics_project/urls.py

from django.contrib import admin
from django.urls import path, include
from logistics_app.views import index, predict_eta, order_create, order_list


#urlpatterns = [
  #  path('admin/', admin.site.urls),
  #  path('', include('logistics_app.urls')),
  #  path('', index, name='home'),
   # path('predict/', predict_eta, name='predict_eta'),
    #path('order/new/', order_create, name='order_create'), 
   # path('orders/', order_list, name='order_list'),
 
#]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('logistics_app.urls')),  # ✅ only once
]

# logistics_project/urls.py