import json
import logging
from pathlib import Path
from typing import Iterable

from django.conf import settings
from django.db import OperationalError, ProgrammingError

from core.plugin.loader import PluginLoader, PluginManifest
from core.plugin.lifecycle import PluginLifecycle
from core.plugin.registry import PluginRegistry
from core.plugin.sdk import PluginAPI
from core.plugin.abi import SUPPORTED_API_VERSIONS

logger = logging.getLogger(__name__)

_registry = PluginRegistry()
_booted = False
_db_ready = False


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
        global _db_ready
        _db_ready = True
    except (OperationalError, ProgrammingError) as exc:
        logger.warning("Plugin boot skipped (database not ready): %s", exc)

    lifecycle = PluginLifecycle(_registry, _api_factory)
    for manifest in _sort_manifests(manifests):
        if not _registry.is_enabled(manifest.name):
            continue
        if manifest.api_version not in SUPPORTED_API_VERSIONS:
            logger.warning(
                "Plugin %s skipped, unsupported api_version: %s",
                manifest.name,
                manifest.api_version,
            )
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


def is_db_ready() -> bool:
    return _db_ready


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


def _load_frontend_manifest(manifest: PluginManifest) -> dict | None:
    if not manifest.root_path:
        return None
    manifest_path = manifest.root_path / "frontend" / "manifest.json"
    if not manifest_path.exists():
        return None
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logger.warning("Invalid frontend manifest for %s", manifest.name)
        return None


def aggregated_manifests() -> list[dict]:
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
                "frontend": _load_frontend_manifest(manifest),
            }
        )
    return results


def all_plugin_states() -> list[dict]:
    results: list[dict] = []
    for state in _registry.list_states():
        manifest = state.manifest
        results.append(
            {
                "name": manifest.name,
                "version": manifest.version,
                "description": manifest.description,
                "dependencies": manifest.dependencies,
                "api_version": manifest.api_version,
                "mount": manifest.mount,
                "enabled": state.enabled,
                "active": state.active,
            }
        )
    return results


def _dependency_map() -> dict[str, list[str]]:
    return {m.name: list(m.dependencies) for m in _registry.manifests()}


def _dependents_map() -> dict[str, list[str]]:
    dependents: dict[str, list[str]] = {m.name: [] for m in _registry.manifests()}
    for plugin, deps in _dependency_map().items():
        for dep in deps:
            dependents.setdefault(dep, []).append(plugin)
    return dependents


def _enable_with_deps(name: str, visiting: set[str]) -> None:
    if name in visiting:
        raise RuntimeError(f"Circular dependency detected at {name}")
    if _registry.is_enabled(name):
        return
    visiting.add(name)
    manifest = _registry.get_manifest(name)
    if manifest.api_version not in SUPPORTED_API_VERSIONS:
        raise RuntimeError(
            f"Unsupported api_version for {name}: {manifest.api_version}"
        )
    for dep in manifest.dependencies:
        _enable_with_deps(dep, visiting)
    visiting.remove(name)

    try:
        from core.models import PluginRecord

        PluginRecord.objects.update_or_create(
            name=name,
            defaults={"version": manifest.version, "enabled": True},
        )
    except (OperationalError, ProgrammingError) as exc:
        logger.warning("Enable plugin skipped (database not ready): %s", exc)
        return

    _registry.set_enabled(name, True)
    if manifest.entry:
        lifecycle = PluginLifecycle(_registry, _api_factory)
        lifecycle.enable(manifest)


def _disable_with_dependents(name: str, visiting: set[str]) -> None:
    if name in visiting:
        raise RuntimeError(f"Circular dependency detected at {name}")
    if not _registry.is_enabled(name):
        return
    visiting.add(name)
    dependents = _dependents_map().get(name, [])
    for dep_name in dependents:
        _disable_with_dependents(dep_name, visiting)
    visiting.remove(name)

    manifest = _registry.get_manifest(name)
    try:
        from core.models import PluginRecord

        PluginRecord.objects.update_or_create(
            name=name,
            defaults={"version": manifest.version, "enabled": False},
        )
    except (OperationalError, ProgrammingError) as exc:
        logger.warning("Disable plugin skipped (database not ready): %s", exc)
        return

    _registry.set_enabled(name, False)
    if _registry.is_active(name):
        lifecycle = PluginLifecycle(_registry, _api_factory)
        lifecycle.disable(manifest)


def enable_plugin(name: str, cascade: bool = True) -> None:
    boot_plugins()
    if cascade:
        _enable_with_deps(name, set())
        return

    manifest = _registry.get_manifest(name)
    missing = [dep for dep in manifest.dependencies if not _registry.is_enabled(dep)]
    if missing:
        raise RuntimeError(f"Missing dependencies: {', '.join(missing)}")
    _enable_with_deps(name, set())


def disable_plugin(name: str, cascade: bool = True) -> None:
    boot_plugins()
    if cascade:
        _disable_with_dependents(name, set())
        return

    if _dependents_map().get(name):
        enabled_dependents = [
            dep for dep in _dependents_map().get(name, []) if _registry.is_enabled(dep)
        ]
        if enabled_dependents:
            raise RuntimeError(f"Dependents still enabled: {', '.join(enabled_dependents)}")

    _disable_with_dependents(name, set())
