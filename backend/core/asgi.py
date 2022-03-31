"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.db import database_sync_to_async

import apps.chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.models import TokenUser


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    @database_sync_to_async
    def get_user(self, id):
        return get_user_model().objects.get(id=id)

    async def __call__(self, scope, receive, send):

        # Copy scope to stop changes going upstream
        scope = dict(scope)

        try:
            headers = dict(scope.get('headers'))
            authorization = headers.get(b'authorization')

            token = AccessToken(authorization.decode().split(' ')[1])
            user_id = TokenUser(token).id

            scope['user'] = await self.get_user(user_id)

        except Exception as auth_exception:
            #print(auth_exception)
            pass

        # Run the inner application along with the scope
        return await self.inner(scope, receive, send)


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": JWTAuthMiddleware(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns
        )
    ),
})
