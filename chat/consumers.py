from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from chat.models import Message

connected_users = {}
connected_channels = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Kada god korisnik udje na web stranicu dodijeljuje mu se random username.
        Svaki korisnik ce biti primljen u globalni chat.
        Prilikom ulaska obavjestavaju se svi aktivni da se pridruzio chatu 
        """
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
        """

        # if self.room_name not in connected_users:
        #     connected_users[self.room_name] = set()
        #     connected_channels[self.room_name] = set()

        connected_users[self.username] = set()

        connected_users[self.username] = self.channel_name
    

        #connected_users[self.room_name].add((self.username,self.channel_name))

        await self.channel_layer.group_send(self.room_name,{
            "type":"users_list",
            "users":list(connected_users)
        })

        await self.accept()

        await self.send(text_data=json.dumps({
            "type":"username_recieve",
            "user":self.username
        }))


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        await self.save_message_to_db(user = self.username,content = message)
        await self.channel_layer.group_send(self.room_name,{
            "type":"chat_message",
            "message":message,
            "user":self.username
        })

        
    async def disconnect(self,code):
        """
        Kada korisnik napusti chat svi u chatu dobiju obavijest o napustanju i 
        dobiju azuriranu listu aktivnih korisnika
        """
        await self.channel_layer.group_send(self.room_name,{
            "type" : "user_group_status",
            "message" : f"{self.username} has left group"
        })

        if self.username in connected_users:
            del connected_users[self.username]

        await self.channel_layer.group_send(
            self.room_name,
        {
            "type":"users_list",
            "message": list(connected_users)
        })

        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )


    async def users_list(self,event):
        await self.send(text_data=json.dumps({
            "type":"users_list",
            "users":list(connected_users)
        }))


    async def user_group_status(self,event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "type":"info_message",
            'message':message
        }))

    async def chat_message(self,event):
        message = event["message"]
        user = event["user"]
        await self.send(text_data = json.dumps({
            'type':"chat_message",
            "message" : message,
            "user" : user
        }))


    @sync_to_async
    def save_message_to_db(self,user,content):
        Message.objects.create(owner=user,content = content)


    @sync_to_async
    def get_messages_from_db(self):
        Message.objects.all()



pairs = {}

class PeerToPeerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user1 = self.scope['url_route']['kwargs']['init_user'] 
        self.user2 = self.scope['url_route']['kwargs']['point_user'] 
        self.room_name=self.user1+"_"+self.user2

        self.accept()
        



