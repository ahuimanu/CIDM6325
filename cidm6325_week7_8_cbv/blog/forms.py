from django import forms
from .models import Post, Comment

FORBIDDEN_WORDS = {'spam', 'scam', 'plagiarism'}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'tags', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows':6}),
        }
    def clean_title(self):
        title = self.cleaned_data['title']
        if any(w in title.lower() for w in FORBIDDEN_WORDS):
            raise forms.ValidationError("Title contains prohibited language.")
        return title
    def clean(self):
        cleaned = super().clean()
        if len((cleaned.get('body') or '')) < 50:
            raise forms.ValidationError("Post body must be at least 50 characters.")
        return cleaned

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'class':'form-control', 'rows':3})}
    def clean_content(self):
        c = self.cleaned_data['content']
        if any(w in c.lower() for w in FORBIDDEN_WORDS):
            raise forms.ValidationError("Please avoid prohibited words.")
        return c
