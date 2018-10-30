from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/', consumers.IndexConsumer),
    path('ws/chat/<room_name>/', consumers.ChatConsumer),
]
