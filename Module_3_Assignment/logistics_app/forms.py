# logistics_app/forms.py 

from django import forms
from .models import Order
from django.utils import timezone


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super(OrderForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Handle read-only case for update view
        if read_only and 'order_id' in self.fields:
            self.fields['order_id'].widget.attrs['readonly'] = True

    class Meta:
        model = Order
        fields = ['customer', 'order_date', 'delivery_location', 'client_type']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'delivery_location': forms.TextInput(attrs={'class': 'form-control'}),
            'client_type': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'customer': 'Customer',
            'order_date': 'Order Date',
            'delivery_location': 'Delivery Location',
            'client_type': 'Client Type',
        }

    def clean_order_date(self):
        order_date = self.cleaned_data.get('order_date')
        if order_date and order_date < timezone.now().date():
            raise forms.ValidationError("Order date cannot be in the past.")
        return order_date

    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get("delivery_location")
        client = cleaned_data.get("client_type")

        if location and client and client.lower() in location.lower():
            raise forms.ValidationError("Client type should not appear in the delivery location.")
        return cleaned_data
