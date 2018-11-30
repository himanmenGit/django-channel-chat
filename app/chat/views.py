import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic.base import View, TemplateView

from .models import Room


class Index(TemplateView):
    template_name = 'chat/index.html'


class RoomView(View):
    def get(self, request, room_name):
        room, created = Room.objects.get_or_create(label=room_name)

        old_messages = room.messages.order_by('timestamp')[:50]
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'old_messages': old_messages,
        })
