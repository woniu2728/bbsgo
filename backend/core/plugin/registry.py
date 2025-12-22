# core/plugin/registry.py
from dataclasses import dataclass
from typing import Dict


@dataclass
class PluginState:
    name: str
    version: str
    enabled: bool = False


class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, PluginState] = {}

    def register(self, state: PluginState) -> None:
        self._plugins[state.name] = state

    def set_enabled(self, name: str, enabled: bool) -> None:
        self._plugins[name].enabled = enabled

    def is_enabled(self, name: str) -> bool:
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not registered")
        return self._plugins[name].enabled

    def enabled_plugin_names(self) -> list[str]:
        return [
            name
            for name, state in self._plugins.items()
            if state.enabled
        ]
