from django.urls import path
from .consumers import ChatConsumer

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    path(r"ws/<str:room>/", consumers.ChatConsumer.as_asgi()),
]