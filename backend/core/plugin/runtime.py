import logging
from pathlib import Path
from typing import Iterable

from django.conf import settings
from django.db import OperationalError, ProgrammingError

from core.plugin.loader import PluginLoader, PluginManifest
from core.plugin.lifecycle import PluginLifecycle
from core.plugin.registry import PluginRegistry
from core.plugin.sdk import PluginAPI

logger = logging.getLogger(__name__)

_registry = PluginRegistry()
_booted = False


def _api_factory(registry: PluginRegistry, plugin_name: str) -> PluginAPI:
    return PluginAPI(registry, plugin_name)


def _sort_manifests(manifests: Iterable[PluginManifest]) -> list[PluginManifest]:
    by_name = {m.name: m for m in manifests}
    deps = {m.name: set(m.dependencies) for m in manifests}
    ordered: list[PluginManifest] = []
    ready = [name for name, items in deps.items() if not items]

    while ready:
        name = ready.pop()
        ordered.append(by_name[name])
        for other_name, other_deps in deps.items():
            if name in other_deps:
                other_deps.remove(name)
                if not other_deps:
                    ready.append(other_name)

    unresolved = [name for name, items in deps.items() if items]
    if unresolved:
        logger.warning("Plugin dependencies unresolved: %s", unresolved)
        for name in unresolved:
            ordered.append(by_name[name])

    return ordered


def get_registry() -> PluginRegistry:
    return _registry


def boot_plugins() -> None:
    global _booted
    if _booted:
        return

    plugins_dir = Path(settings.BASE_DIR) / "plugins"
    loader = PluginLoader(plugins_dir)
    manifests = loader.discover()

    for manifest in manifests:
        _registry.register(manifest)

    try:
        from core.models import PluginRecord

        for manifest in manifests:
            record, created = PluginRecord.objects.get_or_create(
                name=manifest.name,
                defaults={"version": manifest.version, "enabled": True},
            )
            if not created and record.version != manifest.version:
                record.version = manifest.version
                record.save(update_fields=["version"])
            _registry.set_enabled(manifest.name, record.enabled)
    except (OperationalError, ProgrammingError) as exc:
        logger.warning("Plugin boot skipped (database not ready): %s", exc)
        return

    lifecycle = PluginLifecycle(_registry, _api_factory)
    for manifest in _sort_manifests(manifests):
        if not _registry.is_enabled(manifest.name):
            continue
        missing = [dep for dep in manifest.dependencies if not _registry.is_enabled(dep)]
        if missing:
            logger.warning("Plugin %s skipped, missing dependencies: %s", manifest.name, missing)
            continue
        if not manifest.entry:
            continue
        try:
            lifecycle.enable(manifest)
        except Exception as exc:
            logger.exception("Plugin %s failed to enable: %s", manifest.name, exc)

    _booted = True


def enabled_manifests() -> list[dict]:
    results: list[dict] = []
    for state in _registry.list_states():
        if not state.enabled:
            continue
        manifest = state.manifest
        results.append(
            {
                "name": manifest.name,
                "version": manifest.version,
                "description": manifest.description,
                "dependencies": manifest.dependencies,
                "api_version": manifest.api_version,
                "mount": manifest.mount,
            }
        )
    return results
