from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('authors/', views.author_list, name='author_list'),
]