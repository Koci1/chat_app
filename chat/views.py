from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Message
from .serializers import MessageSerializer
from .paginations import MessagePagination
from rest_framework.response import Response
# Create your views here.
def main(request):
    return render(request,"chat/main.html")

class get_messages(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    




