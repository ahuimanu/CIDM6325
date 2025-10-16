from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    Django ModelForm for the Post model.
    Maps 1:1 to all user-editable fields in the Post model.
    """
    
    class Meta:
        model = Post
        fields = ['title', 'author', 'content']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
                'maxlength': '200'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your blog post content here...',
                'rows': 10
            }),
        }
        
        labels = {
            'title': 'Post Title',
            'author': 'Author',
            'content': 'Content',
        }
        
        help_texts = {
            'title': 'Maximum 200 characters',
            'content': 'Write the main content of your blog post',
        }
