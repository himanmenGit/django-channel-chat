from django.urls import path

from . import views

urlpatterns = [
    path('', views.About.as_view(), name='about'),
    path('new/', views.NewRoom.as_view(), name='new-room'),
    path('<label>/', views.ChatRoom.as_view(), name='chat-room'),
]
