# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('usersCommunity/', views.UserCommunityyView.as_view()),
    path('usersCommunity/<int:id>/', views.UserCommunityyView.as_view()),
    path('usersCommunity/<int:id>/update/', views.UserCommunityyView.as_view()),

]