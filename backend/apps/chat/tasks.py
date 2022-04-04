from celery import shared_task

from apps.chat.models import Room, Message


@shared_task
def get_or_create_room(room_name) -> int:
    return Room.objects.get_or_create(name__exact=room_name)[0].id

@shared_task
def message_to_db(user_id, room_name, message):
    message = Message.objects.create(
        user_id=user_id,
        room=Room.objects.get(name__exact=room_name),
        content=message,
    )

@shared_task
def test(x):
    print(x)

@shared_task
def add(x, y):
    print(x + y)
