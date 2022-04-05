from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'created_at']
