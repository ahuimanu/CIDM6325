from django import forms
from .models import Post, Comment, Tag

BANNED_WORDS = {"spam", "clickbait", "scam"}

class PostForm(forms.ModelForm):
    # extra field to let users type tags easily
    tags_csv = forms.CharField(
        label="Tags (comma-separated)", required=False,
        help_text="Example: django, web, tutorial"
    )

    class Meta:
        model = Post
        fields = ["title", "body", "status", "tags_csv"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Clear, descriptive title"}),
            "body": forms.Textarea(attrs={"rows": 8, "aria-describedby": "body-help"}),
        }

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if len(title) < 8:
            raise forms.ValidationError("Title must be at least 8 characters.")
        if any(b in title.lower() for b in BANNED_WORDS):
            raise forms.ValidationError("Title contains disallowed words.")
        return title

    def clean(self):
        data = super().clean()
        title = (data.get("title") or "").strip().lower()
        body = (data.get("body") or "").strip().lower()
        if title and body and body.startswith(title):
            self.add_error("body", "Body should not start by repeating the title verbatim.")
        return data

    def save(self, author, commit=True):
        post = super().save(commit=False)
        post.author = author
        if commit:
            post.save()
            # parse tags_csv into Tag objects
            names = [t.strip() for t in (self.cleaned_data.get("tags_csv") or "").split(",") if t.strip()]
            tag_objs = []
            for name in names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tag_objs.append(tag)
            post.tags.set(tag_objs)
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "Be constructive and courteous."})}

    def clean_body(self):
        body = (self.cleaned_data.get("body") or "")
        if any(b in body.lower() for b in BANNED_WORDS):
            raise forms.ValidationError("Comment contains disallowed words.")
        return body
