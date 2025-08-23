from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .services.chat_service import ChatService
from .constants import INFO_MESSAGE,USERS_LIST,USER_GROUP_STATUS,USERNAME_RECIEVE,USERNAME,USER_JOINED_CHAT,HAS_LEFT_GROUP,CHAT_MESSAGE,OPEN_CHAT,PRIVATE_CHAT_OPEN,MESSAGE,FORCE_DISCONNECT,CONVERSATION_START_WITH
from django.utils import timezone
import json
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
        self.username = self.scope[USERNAME]

        await self.channel_layer.group_add(self.room_name,self.channel_name)

        await self.channel_layer.group_send(self.room_name,{
            "type":USER_GROUP_STATUS,
            MESSAGE:f"{self.username}{USER_JOINED_CHAT}"
        })

        """
        Svi korisnici se dodaju u dict gdje se prati ko je usao i izasao iz chata.
        """

        connected_users[self.username] = self.channel_name
    

        await self.channel_layer.group_send(self.room_name,{
            "type":USERS_LIST,
            "users":list(connected_users)
        })

        await self.accept()

        await self.send(text_data=json.dumps({
            "type":USERNAME_RECIEVE,
            "user":self.username
        }))


    async def receive(self, text_data=None, bytes_data=None):

        """
        Odredjivanje vrste radnje. Da li je normalna poruka ili je poruka za ustpostavu privatnog chata
        """


        data = json.loads(text_data)
        if data.get(MESSAGE):
            message = data[MESSAGE]
            await ChatService.save_message(user = self.username,content = message)
            await self.channel_layer.group_send(self.room_name,{
                "type":CHAT_MESSAGE,
                MESSAGE:message,
                "sender":self.username,
                "timestamp":timezone.now()
            })

        elif data.get("type") == PRIVATE_CHAT_OPEN:
            self.to_user = data.get("to")
            self.from_user = data.get("from")
            self.type = data.get('type')
            self.from_user_channel_name = connected_users[self.to_user]
            if self.from_user_channel_name:
                await self.channel_layer.send(
                    self.from_user_channel_name,
                    {
                        "type" : self.type,
                        "init_user" : self.from_user
                    }
                )

        """
        Preko private_chat_open spajaom i drugog korisnika sa kojim se treba uspostaviti komunikacija
        """
    
    async def private_chat_open(self,event):
        await self.send(text_data=json.dumps({
            "type":OPEN_CHAT,
            "init_user" : event["init_user"]
        }))

        
    async def disconnect(self,code):
        """
        Kada korisnik napusti chat svi u chatu dobiju obavijest o napustanju i 
        dobiju azuriranu listu aktivnih korisnika
        """
        
        await self.channel_layer.group_send(self.room_name,{
            "type" : USER_GROUP_STATUS,
            "message" : f"{self.username} {HAS_LEFT_GROUP}"
        })

        if self.username in connected_users:
            del connected_users[self.username]

        await self.channel_layer.group_send(
            self.room_name,
        {
            "type":USERS_LIST,
            MESSAGE: list(connected_users)
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
            "type":USERS_LIST,
            "users":list(connected_users)
        }))


    async def user_group_status(self,event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "type":INFO_MESSAGE,
            MESSAGE:message
        }))

    async def chat_message(self,event):
        message = event[MESSAGE]
        sender = event["sender"]
        timestamp = event["timestamp"]
        await self.send(text_data = json.dumps({
            'type':CHAT_MESSAGE,
            MESSAGE : message,
            "user" : sender,
            "timestamp" : timestamp.isoformat()
        }))



    """
    Metode za pohranu i dohvatanje poruka sa baze 
    U bazu su ukljucene samo poruke korisnika, a nisu ukljucene system poruke
    """
    # @sync_to_async
    # def save_message_to_db(self,user,content):
    #     Message.objects.create(owner=user,content = content)




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

        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()

        await self.channel_layer.send(
            self.channel_name,
            {
                "type": INFO_MESSAGE, 
                MESSAGE: f"{CONVERSATION_START_WITH} {self.user2}",
            }
)


    async def disconnect(self, close_code):
        """
        Kada se jedan korisnik odspaja odspoji se i drugi automatski
        """
        await self.channel_layer.group_send(
        self.room_name,
        {
            "type": FORCE_DISCONNECT,
        }
    )

        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def force_disconnect(self, event):
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data[MESSAGE]

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": CHAT_MESSAGE,
                MESSAGE: message,
                "sender": self.user1,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            MESSAGE: event[MESSAGE],
            "sender": event["sender"],
        }))

    async def info_message(self, event):
        await self.send(text_data=json.dumps({
            "type":INFO_MESSAGE,
            MESSAGE: event[MESSAGE],
        }))




