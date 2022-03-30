import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Get the room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Create the group name using the room name.
        self.room_group_name = f'chat_{self.room_name}'

        # Creating/Joining a group.
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        """Leave the room."""

        # Remove from the room the the channel from this connection.
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        """Receive the text_data from the Websocket."""

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send an event to a group.
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",  # The name of the method.
                "message": message
            }
        )

    def chat_message(self, event):
        """Send the message to the WebSocket as an event.
        Method to handle an event.
        """
        message = event['message']

        self.send(text_data=json.dumps({
            "message": message
        }))
