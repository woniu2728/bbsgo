from ninja import Router

from plugins.ui_shell.schemas import UiShellManifest

router = Router()


@router.get("/manifest", response=UiShellManifest)
def shell_manifest(request):
    return {
        "menus": [
            {"id": "home", "label": "Home", "path": "/"},
            {"id": "users", "label": "Users", "path": "/users"},
        ],
        "layout": {"name": "default", "regions": ["header", "sidebar", "content"]},
    }
