from django.db import models

import uuid
from django.db import models

class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    order_date = models.DateField()
    delivery_location = models.CharField(max_length=255)
    client_type = models.CharField(max_length=100)
    eta = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            unique_suffix = uuid.uuid4().hex[:6].upper()
            self.order_id = f"ORD-{unique_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} ({self.client_type})"

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
