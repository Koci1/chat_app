from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

connected_users = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Kada god korisnik udje na web stranicu dodijeljuje mu se random username.
        Svaki korisnik ce biti primljen u globalni chat.
        Prilikom ulaska obavjestavaju se svi aktivni da se pridruzio chatu 
        """

        print(self.scope['username'])
        self.room = self.scope['url_route']['kwargs']['room']
        self.room_name = 'chat_%s'%self.room
        self.username = self.scope['username']

        await self.channel_layer.group_add(self.room_name,self.channel_name)

        await self.channel_layer.group_send(self.room_name,{
            "type":"user_group_status",
            "message":f"{self.username} has joined the chat"
        })


        """
        Svi korisnici se dodaju u dict gdje se prati ko je usao i izasao iz chata.
        Takoder, svi 
        
        """

        if self.room_name not in connected_users:
            connected_users[self.room_name] = set()
        
        connected_users[self.room_name].add(self.username)


        await self.channel_layer.group_send(self.room_name,{
            "type":"users_list",
            "users":list(connected_users[self.room_name])
        })

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print(data)


    async def disconnect(self,code):
        await self.channel_layer.group_send(self.room_name,{
            "type" : "user_group_status",
            "message" : f"{self.username} has left group"
        })
        connected_users[self.room_name].discard(self.username)

        await self.channel_layer.group_send(self.room_name,{
            "type":"user_group_status",
            "users":list(connected_users[self.room_name])
        })

        await self.channel_layer.group_discard(self.room_name,
            self.channel_name
        )

    async def users_list(self,event):
        await self.send(text_data=json.dumps({
            "type":"users_list",
            "users": list(connected_users[self.room_name])
        }))

    async def user_left(self,event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "type":"info_message",
            "messsage":message
        }))

    async def user_group_status(self,event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "type":"info_message",
            'message':message
        }))

