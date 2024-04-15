# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('notification/', views.NotificationView.as_view()),
    path('notification/<int:id>/', views.NotificationView.as_view()),
    path('notification/<int:id>/update/', views.NotificationView.as_view()),

]