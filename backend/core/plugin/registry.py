# core/plugin/registry.py
from dataclasses import dataclass
from typing import Dict, Iterable
from core.plugin.loader import PluginManifest


@dataclass
class PluginState:
    manifest: PluginManifest
    enabled: bool = False
    active: bool = False
    mounts: list[str] = None


class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, PluginState] = {}

    def register(self, manifest: PluginManifest) -> None:
        mounts: list[str] = []
        if manifest.mount and isinstance(manifest.mount, dict):
            api_prefix = manifest.mount.get("api_prefix")
            if api_prefix:
                if not api_prefix.startswith("/"):
                    api_prefix = f"/{api_prefix}"
                mounts.append(api_prefix)
        self._plugins[manifest.name] = PluginState(manifest=manifest, mounts=mounts)

    def manifests(self) -> Iterable[PluginManifest]:
        return [state.manifest for state in self._plugins.values()]

    def get_manifest(self, name: str) -> PluginManifest:
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not registered")
        return self._plugins[name].manifest

    def set_enabled(self, name: str, enabled: bool) -> None:
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not registered")
        self._plugins[name].enabled = enabled

    def is_enabled(self, name: str) -> bool:
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not registered")
        return self._plugins[name].enabled

    def set_active(self, name: str, active: bool) -> None:
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not registered")
        self._plugins[name].active = active

    def is_active(self, name: str) -> bool:
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not registered")
        return self._plugins[name].active

    def enabled_plugin_names(self) -> list[str]:
        return [
            name
            for name, state in self._plugins.items()
            if state.enabled
        ]

    def list_states(self) -> list[PluginState]:
        return list(self._plugins.values())

    def add_mount(self, name: str, mount: str) -> None:
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not registered")
        mounts = self._plugins[name].mounts
        if mount not in mounts:
            mounts.append(mount)

    def mounts_for(self, name: str) -> list[str]:
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not registered")
        return list(self._plugins[name].mounts)
