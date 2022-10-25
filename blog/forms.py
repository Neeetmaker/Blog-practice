from django import forms
from .models import Post
from .models import Comm

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)




# Код для комментариев ниже

class CommForm(forms.ModelForm):

    class Meta:
        model = Comm
        fields = ('text',)