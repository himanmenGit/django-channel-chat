from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django_q.brokers import get_broker
from django_q.tasks import async_task as _async

from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']
        self.room_group_name = f'chat_{self.room_name}'
        self.main_group_name = 'main'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user}님이 접속 하셨습니다'
            }
        )
        await self.channel_layer.group_send(
            self.main_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user}님이 접속 하셨습니다'
            }
        )

    async def disconnect(self, code):
        self.user = self.scope['user']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user}님이 퇴장 하셨습니다'
            }
        )
        await self.channel_layer.group_send(
            self.main_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user}님이 퇴장 하셨습니다'
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        self.user = self.scope['user']

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user}: {message}'
            }
        )
        await self.channel_layer.group_send(
            self.main_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user}: {message}'
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))


class IndexConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'main'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        self.user = self.scope['user']

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user}: {message}'
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))


class CusSend:
    def __init__(self):
        self.channel_layer = get_channel_layer()

    def send_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            'main',
            {
                'type': 'chat_message',
                'message': message,
            }
        )
        async_to_sync(self.channel_layer.group_send)(
            'chat_lob',
            {
                'type': 'chat_message',
                'message': message,
            }
        )


def add(message):
    cus = CusSend()
    _async(cus.send_message, message, broker=get_broker('thumb_nail'))
