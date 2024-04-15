# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserView.as_view()),
    path('users/<int:id>/', views.UserView.as_view()),
    path('users/<int:id>/update/', views.UserView.as_view()),
    path('users/authentication/', views.UserPasswordView.as_view()),
]