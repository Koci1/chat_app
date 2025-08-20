"""
ASGI config for chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter,ProtocolTypeRouter
from chat import routing
from chat.middlewares import RandomUsernameMiddleware
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

application = ProtocolTypeRouter(
    {
        'http':get_asgi_application(),
        'websocket': RandomUsernameMiddleware(AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)))
    }
)
