from django import forms
from .models import Post
from .models import Commentary

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)




# Код для комментариев ниже

class CommentaryForm(forms.ModelForm):

    class Meta:
        model = Commentary
        fields = ('text',)