from pathlib import Path
from textwrap import dedent

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a plugin scaffold under backend/plugins"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Plugin name (python package name)")

    def handle(self, *args, **options):
        name = options["name"].strip()
        if not name.isidentifier():
            raise CommandError("Plugin name must be a valid python identifier")

        plugins_dir = Path(settings.BASE_DIR) / "plugins"
        plugin_dir = plugins_dir / name
        if plugin_dir.exists():
            raise CommandError(f"Plugin directory already exists: {plugin_dir}")

        (plugin_dir / "backend").mkdir(parents=True)
        (plugin_dir / "frontend" / "pages").mkdir(parents=True)
        (plugin_dir / "migrations").mkdir(parents=True)

        (plugin_dir / "__init__.py").write_text(
            dedent(
                f"""\
                default_app_config = "plugins.{name}.apps.{name.title().replace('_', '')}Config"
                """
            ),
            encoding="utf-8",
        )
        (plugin_dir / "apps.py").write_text(
            dedent(
                f"""\
                from django.apps import AppConfig


                class {name.title().replace('_', '')}Config(AppConfig):
                    default_auto_field = "django.db.models.BigAutoField"
                    name = "plugins.{name}"
                    label = "{name}"
                """
            ),
            encoding="utf-8",
        )
        (plugin_dir / "plugin.py").write_text(
            dedent(
                """\
                class Plugin:
                    def on_enable(self, api):
                        pass
                """
            ),
            encoding="utf-8",
        )
        (plugin_dir / "plugin.yaml").write_text(
            dedent(
                f"""\
                name: {name}
                version: 0.1.0
                api_version: 1
                entry: plugins.{name}.plugin:Plugin
                description: {name} plugin
                dependencies: []
                mount:
                  api_prefix: /{name}
                """
            ),
            encoding="utf-8",
        )

        (plugin_dir / "backend" / "__init__.py").write_text("", encoding="utf-8")
        (plugin_dir / "backend" / "models.py").write_text(
            "from django.db import models\n",
            encoding="utf-8",
        )
        (plugin_dir / "backend" / "api.py").write_text(
            dedent(
                """\
                from ninja import Router

                router = Router()
                """
            ),
            encoding="utf-8",
        )
        (plugin_dir / "backend" / "permissions.py").write_text(
            "from core.rbac.utils import check_permission\n",
            encoding="utf-8",
        )
        (plugin_dir / "backend" / "hooks.py").write_text(
            "",
            encoding="utf-8",
        )
        (plugin_dir / "frontend" / "manifest.json").write_text(
            dedent(
                f"""\
                {{
                  "name": "{name}",
                  "routes": [
                    {{ "path": "/{name}", "component": "{name.title().replace('_', '')}Home" }}
                  ],
                  "menu": {{ "id": "{name}", "label": "{name.title()}", "path": "/{name}" }}
                }}
                """
            ),
            encoding="utf-8",
        )
        (plugin_dir / "frontend" / "routes.ts").write_text(
            dedent(
                f"""\
                export const routes = [
                  {{ path: "/{name}", component: "{name.title().replace('_', '')}Home" }},
                ];
                """
            ),
            encoding="utf-8",
        )
        (plugin_dir / "frontend" / "pages" / f"{name.title().replace('_', '')}Home.tsx").write_text(
            dedent(
                f"""\
                export function {name.title().replace('_', '')}Home() {{
                  return "{name.title()} Home";
                }}
                """
            ),
            encoding="utf-8",
        )
        (plugin_dir / "migrations" / "__init__.py").write_text("", encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(f"Plugin scaffold created at {plugin_dir}"))
