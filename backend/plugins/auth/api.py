import secrets

from django.contrib.auth import authenticate
from ninja import Router

from plugins.auth.models import AuthToken
from plugins.auth.schemas import AuthManifestOut, LoginIn, TokenOut
from plugins.auth.security import AuthBearer

router = Router()


def _issue_token(user) -> str:
    token = secrets.token_hex(32)
    AuthToken.objects.create(user=user, token=token)
    return token


@router.get("/manifest", response=AuthManifestOut)
def auth_manifest(request):
    return {"token_type": "bearer", "header": "Authorization"}


@router.post("/login", response=TokenOut)
def login(request, payload: LoginIn):
    user = authenticate(request, username=payload.username, password=payload.password)
    if not user:
        return 401, {"detail": "invalid credentials"}
    token = _issue_token(user)
    return {"token": token, "token_type": "bearer"}


@router.post("/refresh", response=TokenOut, auth=AuthBearer())
def refresh_token(request):
    auth_token = request.auth
    auth_token.delete()
    token = _issue_token(auth_token.user)
    return {"token": token, "token_type": "bearer"}
