from core.rbac.utils import check_permission


def can_view(user) -> bool:
    return True


def can_post(user) -> bool:
    return check_permission(user, "forum.post") or getattr(user, "is_authenticated", False)


def can_delete(user) -> bool:
    return check_permission(user, "forum.delete")


def can_manage_boards(user) -> bool:
    return check_permission(user, "admin.forum.manage")
