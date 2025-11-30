# logistics_app/urls.py
from django.urls import path
from .views import index, predict_eta
from .views import (
    OrderListView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    CustomerCreateView,
)

urlpatterns = [
    path('', index, name='index'),
    path('predict/', predict_eta, name='predict_eta'),

    # CBV CRUD routes
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path("customer/create/", CustomerCreateView.as_view(), name="customer_create"),
]
