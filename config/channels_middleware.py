from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from apps.users.models import User
from rest_framework.exceptions import AuthenticationFailed


@database_sync_to_async
def get_user(validated_token):
    try:
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
        except AuthenticationFailed:
            response = {"detail": "Authentication credentials were not provided."}
            await self.send_response(send, response, status=401)
            return

        return await super().__call__(scope, receive, send)

    async def send_response(self, send, response, status):
        # Send the JSON response with the specified status code
        await send({
            "type": "websocket.close",
            "code": status,
            "text": response,
        })


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
