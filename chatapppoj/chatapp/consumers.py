from asgiref.sync import sync_to_async
import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from urllib.parse import parse_qs

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Parse JWT token from query string
        query_string = self.scope['query_string'].decode('utf-8')
        params = parse_qs(query_string)
        token = params.get('token', [None])[0]

        if not token:
            await self.close(code=4001)
            return

        try:
            decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            self.user = await self.get_user(decode_data['user_id'])
            self.scope['user'] = self.user
        except jwt.ExpiredSignatureError:
            await self.close(code=4000)
            return
        except jwt.InvalidTokenError:
            await self.close(code=4001)
            return

        # Corrected key: 'url_route'
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.conversation_id}"

        # Add channel to group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Notify online status
        user_data = await self.get_user_data(self.user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_status',
                'online_users': [user_data],
                'status': 'online'
            }
        )

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            user_data = await self.get_user_data(self.user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'online_status',
                    'online_users': [user_data],
                    'status': 'offline'
                }
            )
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json.get('type')

        if event_type == 'chat_message':
            message_content = text_data_json.get('message')
            user_id = text_data_json.get('user')

            try:
                user = await self.get_user(user_id)
                conversation = await self.get_conversation(self.conversation_id)
                if conversation is None:
                    return

                from .serializers import UserListSerializer
                user_data = UserListSerializer(user).data

                # Save message
                message = await self.save_message(conversation, user, message_content)

                # Broadcast
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message.content,
                        'user': user_data,
                        'timestamp': message.timestamp.isoformat(),
                    }
                )
            except Exception as e:
                print(f"Error: {e}")

        elif event_type == 'typing':
            try:
                user_data = await self.get_user_data(self.user)
                receiver_id = text_data_json.get('receiver')

                if receiver_id and int(receiver_id) != self.user.id:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'typing',
                            'user': user_data,
                            'receiver': int(receiver_id),
                        }
                    )
            except Exception as e:
                print(f"Typing event error: {e}")

    # Event handlers
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def typing(self, event):
        await self.send(text_data=json.dumps(event))

    async def online_status(self, event):
        await self.send(text_data=json.dumps(event))

    # Helper functions
    @sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @sync_to_async
    def get_user_data(self, user):
        from .serializers import UserListSerializer
        return UserListSerializer(user).data

    @sync_to_async
    def get_conversation(self, conversation_id):
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return None

    @sync_to_async
    def save_message(self, conversation, user, content):
        return Message.objects.create(conversation=conversation, sender=user, content=content)
