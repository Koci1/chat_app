from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Message
from .serializers import MessageSerializer
# Create your views here.
def main(request):
    return render(request,"main.html")


class get_messages(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer




