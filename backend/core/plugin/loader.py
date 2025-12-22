# core/plugin/loader.py
from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    entry: str
    description: str | None = None


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

            manifests.append(
                PluginManifest(
                    name=raw["name"],
                    version=raw["version"],
                    entry=raw["entry"],
                    description=raw.get("description"),
                )
            )

        return manifests
