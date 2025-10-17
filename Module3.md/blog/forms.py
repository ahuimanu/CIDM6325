from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Post

MIN_CONTENT_LENGTH = 50

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'aria-describedby': 'title-help'}),
            'content' : forms.Textarea(attrs={'class':'form-control', 'rows':6, 'aria-describedby': 'content-help'}),
        }
        labels = {
            'title': _('Title'),
            'content': _('Content'),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '') or ''
        if len(content.strip()) < MIN_CONTENT_LENGTH:
            raise ValidationError(
                _(f'Post content must be at least {MIN_CONTENT_LENGTH} characters (you typed %(length)s).'),
                code='min_length',
                params={'length': len(content.strip())}
            )
        return content

    def clean_title(self):
        title = self.cleaned_data.get('title', '') or ''
        if len(title.strip()) < 5:
            raise ValidationError(_('Title must be at least 5 characters.'), code='short_title')
        return title
