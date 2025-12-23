from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Router

from core.plugin import events
from plugins.users.schemas import UserCreate, UserOut, UserUpdate

User = get_user_model()

router = Router()


@router.get("/", response=list[UserOut])
def list_users(request):
    return User.objects.all().order_by("id")


@router.get("/{user_id}", response=UserOut)
def get_user(request, user_id: int):
    return get_object_or_404(User, id=user_id)


@router.post("/", response=UserOut)
def create_user(request, payload: UserCreate):
    try:
        user = User.objects.create_user(
            username=payload.username,
            password=payload.password,
            email=payload.email or "",
            display_name=payload.display_name or "",
        )
    except IntegrityError:
        return 400, {"detail": "username already exists"}

    events.emit("user_created", user_id=user.id)
    return user


@router.put("/{user_id}", response=UserOut)
def update_user(request, user_id: int, payload: UserUpdate):
    user = get_object_or_404(User, id=user_id)
    if payload.email is not None:
        user.email = payload.email
    if payload.display_name is not None:
        user.display_name = payload.display_name
    if payload.is_active is not None:
        user.is_active = payload.is_active
    user.save()
    return user


@router.delete("/{user_id}")
def delete_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    events.emit("user_deleted", user_id=user_id)
    return {"ok": True}
