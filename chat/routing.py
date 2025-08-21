from django.urls import path,re_path

from . import consumers

websocket_urlpatterns = [
    path("ws/<str:room>/", consumers.ChatConsumer.as_asgi()),
    re_path(r"^ws/private/(?P<init_user>\w+)/(?P<point_user>\w+)/$", consumers.PeerToPeerConsumer.as_asgi()),
]