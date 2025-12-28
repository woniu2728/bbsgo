# core/plugin/sdk.py
from core.plugin import events
from core.rbac.utils import require_permission


class PluginAPI:
    def __init__(self, registry, plugin_name: str):
        self._registry = registry
        self._plugin_name = plugin_name

    def is_enabled(self, plugin_name: str) -> bool:
        return self._registry.is_enabled(plugin_name)

    def enabled_plugins(self) -> list[str]:
        return self._registry.enabled_plugin_names()

    def add_router(self, router, *, prefix: str | None = None, tags: list[str] | None = None) -> None:
        from core.api import api

        mount_prefix = prefix
        if not mount_prefix:
            manifest = self._registry.get_manifest(self._plugin_name)
            if manifest.mount and isinstance(manifest.mount, dict):
                mount_prefix = manifest.mount.get("api_prefix")
        if not mount_prefix:
            mount_prefix = f"/{self._plugin_name}"
        if not mount_prefix.startswith("/"):
            mount_prefix = f"/{mount_prefix}"
        self._registry.add_mount(self._plugin_name, mount_prefix)
        api.add_router(mount_prefix, router, tags=tags)

    def emit(self, event_name: str, **kwargs):
        events.emit(event_name, **kwargs)

    def subscribe(self, event_name: str, handler):
        events.subscribe(event_name, handler)

    def unsubscribe(self, event_name: str, handler) -> bool:
        return events.unsubscribe(event_name, handler)

    def require_permission(self, permission_code: str):
        return require_permission(permission_code)
