from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import Comm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .forms import CommForm
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})



# Код для комментариев ниже

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = post.comm_set.filter(published_date__lte=timezone.now()).order_by('-published_date')
    if request.method == "POST":
        comment_form = CommForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = Post.objects.get(pk=post.pk)
            comment.author = request.user
            comment.published_date = timezone.now()
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comment': comment, 'comment_form': comment_form})

# ------------------------

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def author_list(request):
    authors = User.objects.all()
    return render(request, 'blog/author_list.html', {'authors': authors})
