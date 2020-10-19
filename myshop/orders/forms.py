from django import forms
from localflavor.us.forms import USZipCodeField    
from .models import Order

class OrderCreateForm(forms.ModelForm):
    """
    Form to create new Order objects    
    """
    postal_code = USZipCodeField()
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']


