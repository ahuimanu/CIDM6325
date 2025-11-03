from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts with image upload
    """
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your blog post content here...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'title': 'Post Title',
            'content': 'Content',
            'image': 'Featured Image (Optional)'
        }
        help_texts = {
            'image': 'Upload an image for your blog post (JPG, PNG, GIF - Max 5MB)'
        }
    
    def clean_image(self):
        """
        Validate uploaded image
        """
        image = self.cleaned_data.get('image')
        
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size cannot exceed 5MB.')
            
            # Check file type
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError(
                    'Invalid file type. Please upload a JPG, PNG, GIF, or WebP image.'
                )
        
        return image
    
    def __init__(self, *args, **kwargs):
        """
        Initialize form and set author if provided
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Remove author field from form - will be set in view
        if 'author' in self.fields:
            del self.fields['author']
