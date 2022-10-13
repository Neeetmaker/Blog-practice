from django.shortcuts import render
from django.utils import timezone
from .models import Post

from django.contrib.auth.models import User

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def author_list(request):
    authors = User.objects.all()
    return render(request, 'blog/author_list.html', {'authors': authors})

"""
def author_list(request):
    authors = User.get_full_name(self)
    return render(request, 'blog/author_list.html', {'authors': authors})
"""
