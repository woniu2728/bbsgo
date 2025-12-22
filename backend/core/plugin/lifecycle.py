# core/plugin/lifecycle.py
import importlib
from core.plugin.registry import PluginRegistry
from core.plugin.loader import PluginManifest


class PluginLifecycle:
    def __init__(self, registry: PluginRegistry, api_factory):
        self._registry = registry
        self._api_factory = api_factory

    def enable(self, manifest: PluginManifest):
        if self._registry.is_enabled(manifest.name):
            raise RuntimeError(f"Plugin {manifest.name} already enabled")
        
        module_path, attr = manifest.entry.split(":")
        module = importlib.import_module(module_path)
        plugin_cls = getattr(module, attr)

        api = self._api_factory(self._registry)
        plugin = plugin_cls()
        plugin.on_enable(api)

        self._registry.set_enabled(manifest.name, True)

    def disable(self, manifest: PluginManifest):
        # Phase 1: disable 只改状态，不做 teardown
        self._registry.set_enabled(manifest.name, False)
