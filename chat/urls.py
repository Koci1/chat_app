from django.urls import path
from .views import main,get_messages
urlpatterns = [
    path('',main),
    path('chat/api/messages/',get_messages().as_view())
]