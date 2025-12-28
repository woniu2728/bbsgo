import logging
from typing import Any

from core.rbac.models import RolePermission, UserRole

logger = logging.getLogger(__name__)


def check_permission(user: Any, permission_code: str) -> bool:
    """
    检查用户是否具有指定权限
    """
    if not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "is_superuser", False):
        return True

    roles = UserRole.objects.filter(user=user).values_list("role_id", flat=True)
    has_permission = RolePermission.objects.filter(
        role_id__in=roles,
        permission__code=permission_code,
    ).exists()
    logger.debug("权限检查: user=%s permission=%s -> %s", getattr(user, "id", "unknown"), permission_code, has_permission)
    return has_permission


def get_request_user(request: Any):
    user = getattr(request, "user", None)
    if user is not None and getattr(user, "is_authenticated", False):
        return user
    auth = getattr(request, "auth", None)
    if auth is not None:
        return getattr(auth, "user", None)
    return None


def require_permission(permission_code: str):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            user = get_request_user(request)
            if not check_permission(user, permission_code):
                return 403, {"detail": "forbidden"}
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def get_user_permissions(user: Any) -> list[str]:
    """
    获取用户的所有权限代码列表
    """
    if not getattr(user, "is_authenticated", False):
        return []

    roles = UserRole.objects.filter(user=user).values_list("role_id", flat=True)
    return list(
        RolePermission.objects.filter(role_id__in=roles)
        .values_list("permission__code", flat=True)
        .distinct()
    )


def get_user_roles(user: Any) -> list[str]:
    """
    获取用户的所有角色名称列表
    """
    if not getattr(user, "is_authenticated", False):
        return []
    return list(UserRole.objects.filter(user=user).values_list("role__name", flat=True))
