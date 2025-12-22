# core/plugin/sdk.py
class PluginAPI:
    def __init__(self, registry):
        self._registry = registry

    def is_enabled(self, plugin_name: str) -> bool:
        return self._registry.is_enabled(plugin_name)

    def enabled_plugins(self) -> list[str]:
        return self._registry.enabled_plugin_names()
