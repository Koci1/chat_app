from django.urls import path

websocket_urlpatterns = [
    path("/ws/<str:room>/")
]