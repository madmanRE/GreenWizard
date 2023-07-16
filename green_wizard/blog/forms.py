from django import forms
from .models import Post, Review


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'main_img', 'p1', 'img1', 'p2', 'img2', 'p3', 'img3', 'other_text')

        def __init__(self, *args, **kwargs):
            self.author = kwargs.pop("author", None)
            super().__init__(*args, **kwargs)

        def save(self, commit=True):
            post = super().save(commit=False)
            post.author = self.author
            if commit:
                post.save()
            return post


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(
                attrs={"class": "form-textarea", "placeholder": "Отзыв"}
            )
        }

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        review = super().save(commit=False)
        review.author = self.author
        if commit:
            review.save()
        return review
