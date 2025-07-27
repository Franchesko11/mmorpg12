from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView, ResponseCreateView,
    ResponseListView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('category/<slug:category_slug>/', PostListView.as_view(), name='post_list_by_category'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/response/', ResponseCreateView.as_view(), name='response_create'),
    path('responses/', ResponseListView.as_view(), name='response_list'),
]