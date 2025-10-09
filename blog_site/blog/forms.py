from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    ModelForm for creating and updating Post instances.
    Maps 1:1 to the Post model.
    """
    class Meta:
        model = Post
        fields = ['title', 'body', 'publish_date', 'tags']
        widgets = {
            'publish_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }