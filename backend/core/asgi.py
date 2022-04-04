"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
import os

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.models import TokenUser

from django.core.asgi import get_asgi_application
from django.utils.functional import LazyObject
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from channels.middleware import BaseMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.db import database_sync_to_async

import apps.chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


@database_sync_to_async
def get_user(scope):
    try:
        headers = dict(scope.get('headers'))
        authorization = headers.get(b'authorization')

        token = AccessToken(authorization.decode().split(' ')[1])
        user_id = TokenUser(token).id
        user = get_user_model().objects.get(id=user_id)

    except Exception as UnauthenticatedUser:
        user = AnonymousUser()

    return user


class UserLazyObject(LazyObject):
    """
    Throw a more useful error message when scope['user'] is accessed before
    it's resolved
    """

    def _setup(self):
        raise ValueError("Accessing scope user before it is ready.")


class JWTAuthMiddleware(BaseMiddleware):
    def populate_scope(self, scope):
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        scope["user"]._wrapped = await get_user(scope=scope)

    async def __call__(self, scope, receive, send):
        # Copy scope to stop changes going upstream
        scope = dict(scope)

        # Scope injection/mutation per this middlware's needs.
        self.populate_scope(scope)

        # Grab the finalized/resolved scope
        await self.resolve_scope(scope)

        # Run the inner application along with the scope
        return await super().__call__(scope, receive, send)


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": JWTAuthMiddleware(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns
        )
    ),
})
