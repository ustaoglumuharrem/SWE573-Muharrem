# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('communityTemplate/', views.CommunityTemplateView.as_view()),
    path('communityTemplate/<int:id>/', views.CommunityTemplateView.as_view()),
    path('communityTemplate/<int:id>/update/', views.CommunityTemplateView.as_view()),

]