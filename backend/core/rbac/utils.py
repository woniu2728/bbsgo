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

    roles = UserRole.objects.filter(user=user).values_list("role_id", flat=True)
    has_permission = RolePermission.objects.filter(
        role_id__in=roles,
        permission__code=permission_code,
    ).exists()
    logger.debug("权限检查: user=%s permission=%s -> %s", getattr(user, "id", "unknown"), permission_code, has_permission)
    return has_permission


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
