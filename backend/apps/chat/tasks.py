from celery import shared_task
from apps.chat.models import Room, Message


@shared_task
def get_or_create_room(room_name) -> int:
    try:
        room_object = Room.objects.get(name=room_name)
    except Exception:
        room_object = Room(name=room_name)
        room_object.save()

    return room_object.id

@shared_task
def get_room_messages(room):
    room_message_objs = Message.objects.filter(
        room=room
    )
    return [(msg.user.username, msg.content) for msg in room_message_objs]

@shared_task
def message_to_db(user, room, message):
    message = Message(
        user=user,
        room=room,
        content=message,
    )
    message.save()
    return message.id
