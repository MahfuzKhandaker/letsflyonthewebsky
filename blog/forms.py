from django import forms
from pagedown.widgets import AdminPagedownWidget
from blog.models import Post


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=AdminPagedownWidget())
    class Meta:
        model = Post
        fields = ['title', 'slug', 'summary', 'body', 'main_image', 'categories',]


class CommentForm(forms.Form):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!",
            "rows": "5"
        })
    )