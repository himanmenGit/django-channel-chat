from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateView

from haikunator import Haikunator

from .models import Room


class About(TemplateView):
    template_name = 'chat/about.html'


class NewRoom(View):
    http_method_names = ['get']

    def get(self, request):
        new_room = None
        while not new_room:
            with transaction.atomic():
                label = Haikunator.haikunate()
                if not Room.objects.filter(label=label).exists():
                    new_room = Room.objects.create(label=label)
        return redirect(ChatRoom, label=label)


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
