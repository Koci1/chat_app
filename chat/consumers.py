from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Kada god korisnik udje na web stranicu dodijeljuje mu se random username.
        Svaki korisnik ce biti primljen u globalni chat.
        Prilikom ulaska obavjestavaju se svi aktivni da se pridruzio chatu 
        """

        print(self.scope['username'])
        self.room = self.scope['global_room']
        self.room_name = 'chat_%s'%self.room
        self.username = self.scope['username']

        await self.channel_layer.group_add(self.room_name,self.channel_name)

        await self.channel_layer.group_send(self.room_name,{
            "type":"new_user_join",
            "message":f"{self.username} has joined the chat"
        })

        await self.accept()

