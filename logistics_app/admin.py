from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Order, Customer

# Custom Action
def mark_as_delivered(modeladmin, request, queryset):
    queryset.update(client_type='Delivered')  # Adjust if needed
mark_as_delivered.short_description = "Mark selected orders as Delivered"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'order_date',
        'client_type',
        'delivery_location',
        'order_form_link'
    )
    search_fields = ('order_id', 'client_type', 'delivery_location')
    list_filter = ('client_type', 'order_date')  # 'status' removed
    ordering = ('-order_date',)
    readonly_fields = ('order_date',)
    list_per_page = 25
    actions = [mark_as_delivered]

    def order_form_link(self, obj):
        url = reverse("order_create")
        return format_html('<a class="button" href="{}">Create New Order</a>', url)
    order_form_link.short_description = "Create Order"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')  # Removed created_at and orders_link
    search_fields = ('name', 'email', 'phone')
    list_per_page = 20
