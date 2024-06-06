from django import forms

from . models import Blog

class PostBlog(forms.ModelForm):
    class Meta:
        model = Blog
        fields =['title', 'content', 'image','type']

