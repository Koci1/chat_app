from chat.models import Message
from asgiref.sync import sync_to_async

class ChatService:

    @staticmethod
    @sync_to_async
    def save_message(user,content):
        Message.objects.create(owner = user,content = content)
