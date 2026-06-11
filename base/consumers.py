import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils.timezone import localtime
from .models import Room, Message 

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_room_{self.room_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        user = self.scope['user']

        if(not user.is_authenticated):
            return
        
        action = text_data_json.get('action')
        
        if action == 'typing':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_typing_broadcast',
                    'user_id': user.id if user.is_authenticated else None,
                    'username': user.username if user.is_authenticated else 'Anonymous',
                    'is_typing': text_data_json.get('is_typing', False)
                }
            )
            return
        
        message_body = text_data_json['message']
        message_id = None
        created_time_str = localtime().strftime('%I:%M %p')

        if user.is_authenticated:
            room = Room.objects.get(id=self.room_id)
            
            new_msg = Message.objects.create(
                user=user,
                room=room,
                body=message_body
            )
            room.participants.add(user)
            
            message_id = new_msg.id
            created_time_str = new_msg.created.isoformat()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_body,
                'username': user.username if user.is_authenticated else 'Anonymous',
                'user_id': user.id if user.is_authenticated else '',
                'avatar_url': user.avatar_url if user.is_authenticated else '/media/avatar.svg',
                'message_id': message_id,
                'created_time': created_time_str
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'action': 'create',
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'avatar_url': event['avatar_url'],
            'message_id': event.get('message_id') ,
            'created_time': event['created_time']
        }))

    def message_deleted_broadcast(self, event):
        self.send(text_data=json.dumps({
            'action': 'delete',
            'message_id': event['message_id']
        }))

    def user_typing_broadcast(self, event):
        self.send(text_data=json.dumps({
            'action': 'typing',
            'user_id': event['user_id'],
            'username': event['username'],
            'is_typing': event['is_typing']
        }))

