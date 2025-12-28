"""
Core API - 插件系统集成核心接口
职责：提供插件路由挂载等基础功能，不包含插件管理逻辑
"""
from ninja import NinjaAPI, Router, Schema
from core.plugin.runtime import boot_plugins, aggregated_manifests, disable_plugin, enable_plugin

# 核心API实例
api = NinjaAPI(title="Forum Core API", version="1.0.0")

router = Router()


@router.get("/plugins/manifests")
def plugin_manifests(request):
    boot_plugins()
    return {"plugins": aggregated_manifests()}


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
