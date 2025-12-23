# core/plugin/sdk.py
from core.plugin import events


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

        mount_prefix = prefix or f"/{self._plugin_name}"
        api.add_router(mount_prefix, router, tags=tags)

    def emit(self, event_name: str, **kwargs):
        events.emit(event_name, **kwargs)

    def subscribe(self, event_name: str, handler):
        events.subscribe(event_name, handler)
