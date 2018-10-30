import json

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic.base import View, TemplateView

from .models import Room


class Index(TemplateView):
    template_name = 'chat/index.html'


class RoomView(View):
    def get(self, request, room_name):
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name))
        })


class ChatRoom(View):
    def get(self, request, label):
        room, created = Room.objects.get_or_create(label=label)
        messages = reversed(room.messages.order_by('timestamp')[:50])
        print('GET' * 20)
        return render(request, 'chat/room.html', {'room': room, 'messages': messages})

    def post(self, request, label):
        room, created = Room.objects.get_or_create(label=label)
        messages = reversed(room.messages.order_by('timestamp')[:50])
        print('POSt' * 20)
        return render(request, 'chat/room.html', {'room': room, 'messages': messages})
