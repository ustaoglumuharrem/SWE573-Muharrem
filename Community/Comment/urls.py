# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('comment/', views.CommentView.as_view()),
    path('comment/<int:id>/', views.CommentView.as_view()),
    path('comment/<int:id>/update/', views.CommentView.as_view()),
    path('comment/<int:id>/upvote/', views.CommentView.as_view()),  # URL for upvoting
    path('comment/<int:id>/downvote/', views.CommentView.as_view()),  # URL for downvoting
    path('comments/', views.CommentListView.as_view(), name='comment-list'),


]