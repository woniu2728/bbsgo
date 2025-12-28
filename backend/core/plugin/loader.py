# core/plugin/loader.py
from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    entry: str | None
    dependencies: list[str]
    description: str | None = None
    api_version: int | None = None
    mount: dict | None = None
    root_path: Path | None = None


class PluginLoader:
    def __init__(self, plugins_dir: Path):
        self.plugins_dir = plugins_dir

    def discover(self) -> list[PluginManifest]:
        manifests: list[PluginManifest] = []

        for plugin_dir in self.plugins_dir.iterdir():
            if not plugin_dir.is_dir():
                continue
            manifest_path = plugin_dir / "plugin.yaml"
            if not manifest_path.exists():
                continue

            with open(manifest_path, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f)

            dependencies = raw.get("dependencies") or []
            if not isinstance(dependencies, list):
                raise ValueError(f"Plugin {raw.get('name')} dependencies must be a list")

            manifests.append(
                PluginManifest(
                    name=raw["name"],
                    version=raw["version"],
                    entry=raw.get("entry"),
                    dependencies=dependencies,
                    description=raw.get("description"),
                    api_version=raw.get("api_version"),
                    mount=raw.get("mount"),
                    root_path=plugin_dir,
                )
            )

        return manifests
