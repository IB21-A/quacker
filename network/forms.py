from django.forms import ModelForm, Textarea
from .models import Post
from django import forms

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        widgets = {
            'body': Textarea(attrs={'class': "form-control", 
                                    'id': "post-body", 
                                    'placeholder': "Write your post here!",
                                    'rows': 7})
        }
        
        