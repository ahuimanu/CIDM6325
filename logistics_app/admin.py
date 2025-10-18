from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Order, Customer

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_date', 'client_type', 'delivery_location')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

def order_form_link(self, obj):
        url = reverse("order_create")  # name from your urls.py
        return format_html('<a class="button" href="{}">Create New Order</a>', url)
order_form_link.short_description = "Order Form"