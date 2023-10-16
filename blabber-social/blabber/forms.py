# blabber/forms.py

from django import forms
from .models import Blab

class DweetForm(forms.ModelForm):
    body = forms.CharField(required=True)

    # https://docs.djangoproject.com/en/3.2/topics/db/models/#meta-options
    class Meta:
        model = Blab
        exclude = ("user", )