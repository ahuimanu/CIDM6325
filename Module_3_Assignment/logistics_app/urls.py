# logistics_app/urls.py

from django.urls import path
from .views import index, predict_eta, order_create, order_list, order_update, order_delete

urlpatterns = [
    path('', index, name='index'),
    path('predict/', predict_eta, name='predict_eta'),
    path('order/create/', order_create, name='order_create'),
    path('orders/', order_list, name='order_list'),
    path('order/<int:pk>/update/', order_update, name='order_update'),
    path('order/<int:pk>/delete/', order_delete, name='order_delete'),
]
