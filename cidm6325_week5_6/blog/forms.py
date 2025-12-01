from django import forms
from .models import Post, Comment

FORBIDDEN_WORDS = {'spam', 'scam', 'plagiarism'}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'tags', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby':'titleHelp'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows':6}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if any(word in title.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Title contains prohibited language.")
        return title

    def clean(self):
        cleaned = super().clean()
        body = cleaned.get('body', '') or ''
        if len(body) < 50:
            raise forms.ValidationError("Post body must be at least 50 characters for substance.")
        return cleaned

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'aria-label':'Comment'})
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        if any(word in content.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Please avoid prohibited words.")
        return content
