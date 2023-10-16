# blabber/forms.py

from django import forms
from .models import Blab

class BlabForm(forms.ModelForm):
    body = forms.CharField(
        required = True,
        widget = forms.widgets.Textarea(
            attrs = {
                "placeholder": "I dare you to shut your trap...",
                "class": "form-control",
            }
        ),
        label = "",
    )

    # https://docs.djangoproject.com/en/3.2/topics/db/models/#meta-options
    class Meta:
        model = Blab
        exclude = ("user", )