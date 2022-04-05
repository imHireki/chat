from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .models import Message, Room
from .serializers import MessageSerializer


class MessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, room, format=None):
        room = Room.objects.get(name=room)
        messages = Message.objects.filter(room=room)

        serializer = MessageSerializer(messages, many=True)
        return Response({'messages': serializer.data})
