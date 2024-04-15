# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('communityy/', views.CommunityyView.as_view()),
    path('communityy/<int:id>/', views.CommunityyView.as_view()),
    path('communityy/<int:id>/update/', views.CommunityyView.as_view()),

]