# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.PostView.as_view()),
    path('post/<int:id>/', views.PostView.as_view()),
    path('post/<int:id>/update/', views.PostView.as_view()),
    path('posts/', views.PostListView.as_view(), name='post-list'),

]