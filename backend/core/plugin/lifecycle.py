# core/plugin/lifecycle.py
import importlib
from core.plugin.registry import PluginRegistry
from core.plugin.loader import PluginManifest


class PluginLifecycle:
    def __init__(self, registry: PluginRegistry, api_factory):
        self._registry = registry
        self._api_factory = api_factory

    def enable(self, manifest: PluginManifest):
        if self._registry.is_active(manifest.name):
            raise RuntimeError(f"Plugin {manifest.name} already active")
        if not manifest.entry:
            raise RuntimeError(f"Plugin {manifest.name} has no entry to enable")
        
        module_path, attr = manifest.entry.split(":")
        module = importlib.import_module(module_path)
        plugin_cls = getattr(module, attr)

        api = self._api_factory(self._registry, manifest.name)
        plugin = plugin_cls()
        plugin.on_enable(api)
        self._registry.set_instance(manifest.name, plugin)
        self._registry.set_active(manifest.name, True)

    def disable(self, manifest: PluginManifest):
        plugin = self._registry.get_instance(manifest.name)
        if plugin and hasattr(plugin, "on_disable"):
            api = self._api_factory(self._registry, manifest.name)
            try:
                plugin.on_disable(api)
            except Exception:
                # Keep disable flow safe while surfacing error in logs
                import logging

                logging.getLogger(__name__).exception(
                    "Plugin %s on_disable failed", manifest.name
                )
        self._registry.set_active(manifest.name, False)
        self._registry.set_instance(manifest.name, None)
