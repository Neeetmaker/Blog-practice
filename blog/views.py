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
from django.db.models import Q
from django.core.paginator import Paginator

#Код пагинации в списке постов

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    posts_paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_object = posts_paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'posts': page_object})


# Код для комментариев ниже

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

# Код счетчика просмотров

    post.views_count = post.views_count + 1
    post.save()

# ======================

# Код для блока с наиболее популярными постами

    popular_posts = Post.objects.filter(views_count__gte=1)
    #posts_paginator = Paginator(popular_posts, 3)
    #page_number = request.GET.get('page')
    #page_object = posts_paginator.get_page(page_number)

# ============================================

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
    return render(request, 'blog/post_detail.html', {'post': post, 'popular_posts': popular_posts, 'comments': comments, 'comment_form': comment_form})

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

# Код профиля автора

def author_detail(request, pk):
    author = get_object_or_404(User, pk=pk)
    author_posts = author.post_set.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/author_detail.html', {'author': author, 'author_posts': author_posts})

# Код поиска по заголовку

def search_results(request):
    search_query = request.GET['search']
    queryset = Post.objects.filter(
        Q(title__icontains=search_query) | 
        Q(text__icontains=search_query) | 
        Q(author__username__icontains=search_query) , published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/search_results.html', {'search_query': search_query ,'posts': queryset})