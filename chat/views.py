from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Message
from .serializers import MessageSerializer
from .paginations import MessagePagination
from .constants import TEMPLATE_MAIN

# Create your views here.
def main(request):
    return render(request,TEMPLATE_MAIN)

class get_messages(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    




