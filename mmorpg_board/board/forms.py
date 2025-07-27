from django import forms
from .models import Post, Response
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }