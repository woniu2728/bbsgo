import importlib
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.plugin.loader import PluginLoader
from core.plugin.abi import SUPPORTED_API_VERSIONS


class Command(BaseCommand):
    help = "Validate plugin manifests, dependencies, entries, and frontend manifests"

    def handle(self, *args, **options):
        plugins_dir = Path(settings.BASE_DIR) / "plugins"
        loader = PluginLoader(plugins_dir)
        manifests = loader.discover()

        if not manifests:
            self.stdout.write("No plugins found.")
            return

        names = {m.name for m in manifests}
        errors: list[str] = []
        warnings: list[str] = []
        used_prefixes: dict[str, str] = {}
        used_routes: dict[str, str] = {}
        used_menu_ids: dict[str, str] = {}

        for manifest in manifests:
            plugin_root = manifest.root_path
            init_py = plugin_root / "__init__.py" if plugin_root else None
            if init_py and not init_py.exists():
                warnings.append(f"{manifest.name}: missing __init__.py (auto registration will skip)")

            for dep in manifest.dependencies:
                if dep not in names:
                    errors.append(f"{manifest.name}: missing dependency {dep}")

            if manifest.api_version not in SUPPORTED_API_VERSIONS:
                errors.append(
                    f"{manifest.name}: unsupported api_version {manifest.api_version}"
                )

            if manifest.entry:
                if ":" not in manifest.entry:
                    errors.append(f"{manifest.name}: entry should be module:Class")
                else:
                    module_path, attr = manifest.entry.split(":", 1)
                    try:
                        module = importlib.import_module(module_path)
                        if not hasattr(module, attr):
                            errors.append(f"{manifest.name}: entry attribute {attr} not found in {module_path}")
                    except Exception as exc:
                        errors.append(f"{manifest.name}: entry import failed: {exc}")

            api_prefix = None
            if manifest.mount and isinstance(manifest.mount, dict):
                api_prefix = manifest.mount.get("api_prefix")
            if api_prefix:
                if not api_prefix.startswith("/"):
                    warnings.append(f"{manifest.name}: api_prefix should start with '/'")
                if api_prefix in used_prefixes:
                    errors.append(
                        f"{manifest.name}: api_prefix conflicts with {used_prefixes[api_prefix]}"
                    )
                else:
                    used_prefixes[api_prefix] = manifest.name

            frontend_manifest = (
                plugin_root / "frontend" / "manifest.json" if plugin_root else None
            )
            if frontend_manifest and frontend_manifest.exists():
                try:
                    frontend_data = json.loads(
                        frontend_manifest.read_text(encoding="utf-8")
                    )
                except json.JSONDecodeError as exc:
                    errors.append(f"{manifest.name}: invalid frontend manifest: {exc}")
                else:
                    routes = frontend_data.get("routes") or []
                    if isinstance(routes, list):
                        for route in routes:
                            path = route.get("path") if isinstance(route, dict) else None
                            if not path:
                                continue
                            if path in used_routes:
                                errors.append(
                                    f"{manifest.name}: route path {path} conflicts with {used_routes[path]}"
                                )
                            else:
                                used_routes[path] = manifest.name
                    menu = frontend_data.get("menu")
                    if isinstance(menu, dict):
                        menu_id = menu.get("id")
                        if menu_id:
                            if menu_id in used_menu_ids:
                                errors.append(
                                    f"{manifest.name}: menu id {menu_id} conflicts with {used_menu_ids[menu_id]}"
                                )
                            else:
                                used_menu_ids[menu_id] = manifest.name

        if warnings:
            self.stdout.write("Warnings:")
            for item in warnings:
                self.stdout.write(f"- {item}")

        if errors:
            self.stdout.write("Errors:")
            for item in errors:
                self.stdout.write(f"- {item}")
            raise CommandError("Plugin validation failed.")

        self.stdout.write(self.style.SUCCESS("All plugins validated successfully."))
