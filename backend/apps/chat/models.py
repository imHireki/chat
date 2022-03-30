from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
CASCADE = models.CASCADE


class Room(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    room = models.ForeignKey(Room, on_delete=CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
