from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from chat.models import Message
from .services.chat_service import ChatService

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

        connected_users[self.username] = self.channel_name
    

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

        """
        Odredjivanje vrste radnje. Da li je normalna poruka ili je poruka za ustpostavu privatnog chata
        """


        data = json.loads(text_data)
        if data.get("message"):
            message = data["message"]
            await ChatService.save_message(user = self.username,content = message)
            await self.channel_layer.group_send(self.room_name,{
                "type":"chat_message",
                "message":message,
                "sender":self.username
            })

        elif data.get("type") == 'private_chat_open':
            self.to_user = data.get("to")
            self.from_user = data.get("from")
            self.type = data.get('type')
            self.from_user_channel_name = connected_users[self.to_user]
            if self.from_user_channel_name:
                await self.channel_layer.send(
                    self.from_user_channel_name,
                    {
                        "type" : self.type, #private_chat_open 
                        "init_user" : self.from_user
                    }
                )
    
    async def private_chat_open(self,event):
        await self.send(text_data=json.dumps({
            "type":"open_chat",
            "init_user" : event["init_user"]
        }))

        
    async def disconnect(self,code):
        """
        Kada korisnik napusti chat svi u chatu dobiju obavijest o napustanju i 
        dobiju azuriranu listu aktivnih korisnika
        """

        print("Korisnik se iskljucuje")

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
        """
        Svakom korisnku se prilikom prijave novog korisnika osvjezi lista
        """
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
        sender = event["sender"]
        await self.send(text_data = json.dumps({
            'type':"chat_message",
            "message" : message,
            "user" : sender
        }))



    """
    Metode za pohranu i dohvatanje poruka sa baze 
    U bazu su ukljucene samo poruke korisnika, a nisu ukljucene system poruke
    
    """
    @sync_to_async
    def save_message_to_db(self,user,content):
        Message.objects.create(owner=user,content = content)


    # @sync_to_async
    # def get_messages_from_db(self):
    #     Message.objects.all()



pairs = {}

class PeerToPeerConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        """
        Prilikom uspostave privatnog chata i jedan i drugi korisnik dobijaju sobu sa istim imenom
        """

        self.user1 = self.scope['url_route']['kwargs']['init_user']
        self.user2 = self.scope['url_route']['kwargs']['point_user']

        # Room name po kombinaciji korisnika
        users_sorted = sorted([self.user1, self.user2])
        self.room_name = f"chat_{users_sorted[0]}_{users_sorted[1]}"

        # dodaj sebe u grupu
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        # Prihvati konekciju
        await self.accept()

    async def disconnect(self, close_code):
        # Očisti grupu
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Pošalji poruku u room grupu
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.user1,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))



