from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from apps.users.models import User
from rest_framework_simplejwt.exceptions import InvalidToken

@database_sync_to_async
def get_user(validated_token):
    try:
        print("User id", validated_token["user_id"])
        return User.objects.get(id=validated_token["user_id"])
    except User.DoesNotExist:
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query = dict((x.split("=") for x in scope["query_string"].decode().split("&")))
        try:
            validated_token = JWTTokenUserAuthentication().get_validated_token(
                raw_token=query.get("token")
            )
            scope["user"] = await get_user(validated_token=validated_token)
        except InvalidToken:
            scope["user"] = AnonymousUser()
        print("scope", scope['user'])
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
