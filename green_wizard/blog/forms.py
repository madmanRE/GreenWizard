from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'author', 'main_img', 'p1', 'img1', 'p2', 'img2', 'p3', 'img3', 'other_text')