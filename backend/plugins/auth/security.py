from ninja.security import HttpBearer

from plugins.auth.models import AuthToken


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        auth_token = AuthToken.objects.select_related("user").filter(token=token).first()
        if not auth_token:
            return None
        return auth_token
