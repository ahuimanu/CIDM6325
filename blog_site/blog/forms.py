from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    ModelForm for creating and updating Post instances.
    Maps 1:1 to the Post model.
    """

    class Meta:
        model = Post
        fields = ["title", "body", "publish_date", "tags"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control markdown-editor",  # Bootstrap + EasyMDE hook
                    "rows": 14,
                    "placeholder": "Write your post in Markdown…",
                }
            ),
            "publish_date": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Post title"}),
            "tags": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Tags (comma separated)"}
            ),
        }
        help_texts = {
            "body": "Supports Markdown. HTML will be sanitized on render.",
        }
