import datetime
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import Commentary
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .forms import CommentaryForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# Вот это я хуйню сделал, пиздец

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


# Код для комментариев ниже

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.commentary_set.filter(published_date__lte=timezone.now()).order_by('-published_date')
    if request.method == "POST":
        comment_form = CommentaryForm(request.POST)
        if comment_form.is_valid():
            comments = comment_form.save(commit=False)
            comments.post = post
            comments.author = request.user
            comments.published_date = timezone.now()
            comments.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentaryForm() 
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

# Код удаление комментария

def comm_delete(request, pk):
    comment_delete = get_object_or_404(Commentary, pk=pk)
    comment_delete.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Код редактирования коментария

def comm_edit(request, pk):
    comment_edit = get_object_or_404(Commentary, pk=pk)
    if timezone.now() - comment_edit.created_date <= datetime.timedelta(minutes=30):
        if request.method == "POST": 
            comment_form = CommentaryForm(request.POST, instance=comment_edit)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.published_date = timezone.now()
                comment.save()
                return redirect('post_detail', pk=comment.post.pk)
        else:
            comment_form = CommentaryForm(instance=comment_edit)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'blog/comm_edit.html', {'comment_form': comment_form, 'comment_edit': comment_edit})

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
    commtest = Commentary.objects.all()
    return render(request, 'blog/author_list.html', {'authors': authors, 'commtest': commtest})
