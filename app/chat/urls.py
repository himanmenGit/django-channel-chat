from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<room_name>/', views.RoomView.as_view(), name='room'),
]
