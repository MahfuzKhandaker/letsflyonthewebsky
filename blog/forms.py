from django import forms
from pagedown.widgets import AdminPagedownWidget
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=AdminPagedownWidget())
    class Meta:
        model = Post
        fields = ['title', 'slug', 'summary', 'body', 'main_image', 'image_caption', 'categories']


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write Somethings Here!',
        'rows': '4',
        'cols': '50'
    }))
    class Meta:
        model = Comment
        fields = ('content',)