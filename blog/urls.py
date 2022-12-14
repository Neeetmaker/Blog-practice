from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('comm_delete/<int:pk>/', views.comm_delete, name='comm_delete'),
    path('comm_edit/<int:pk>/', views.comm_edit, name='comm_edit'),
    path('search_results/', views.search_results, name='search_results'),
    path('author_detail/<int:pk>/', views.author_detail, name='author_detail'),
]