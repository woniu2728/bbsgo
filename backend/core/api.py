"""
Core API - 插件系统集成核心接口
职责：提供插件路由挂载等基础功能，不包含插件管理逻辑
"""
from ninja import NinjaAPI, Router, Schema
from core.plugin.runtime import (
    aggregated_manifests,
    all_plugin_states,
    boot_plugins,
    disable_plugin,
    enable_plugin,
)
from core.rbac.utils import check_permission
from plugins.auth.security import AuthBearer

# 核心API实例
api = NinjaAPI(title="Forum Core API", version="1.0.0")

router = Router()


@router.get("/plugins/manifests")
def plugin_manifests(request):
    boot_plugins()
    return {"plugins": aggregated_manifests()}


@router.get("/plugins", auth=AuthBearer())
def plugin_states(request):
    if not check_permission(request.auth.user, "admin.plugins.manage"):
        return 403, {"detail": "forbidden"}
    boot_plugins()
    return {"plugins": all_plugin_states()}


class PluginToggleIn(Schema):
    name: str
    cascade: bool = True


@router.post("/plugins/enable")
def enable_plugin_api(request, payload: PluginToggleIn):
    try:
        enable_plugin(payload.name, cascade=payload.cascade)
    except KeyError:
        return 404, {"detail": "plugin not found"}
    except RuntimeError as exc:
        return 400, {"detail": str(exc)}
    return {"ok": True, "name": payload.name, "enabled": True}


@router.post("/plugins/disable")
def disable_plugin_api(request, payload: PluginToggleIn):
    try:
        disable_plugin(payload.name, cascade=payload.cascade)
    except KeyError:
        return 404, {"detail": "plugin not found"}
    except RuntimeError as exc:
        return 400, {"detail": str(exc)}
    return {"ok": True, "name": payload.name, "enabled": False}


api.add_router("", router)
