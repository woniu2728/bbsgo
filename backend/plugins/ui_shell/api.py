from ninja import Router
from plugins.auth.security import AuthBearer
from core.rbac.utils import check_permission
from plugins.ui_shell.models import UiShellSettings
from plugins.ui_shell.schemas import SeoOut, SeoUpdate, ThemeOut, ThemeUpdate

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


def _get_settings() -> UiShellSettings:
    settings = UiShellSettings.objects.first()
    if settings:
        return settings
    return UiShellSettings.objects.create()


@router.get("/theme", response=ThemeOut)
def get_theme(request):
    settings = _get_settings()
    return {"theme": settings.theme}


@router.post("/theme", response=ThemeOut, auth=AuthBearer())
def update_theme(request, payload: ThemeUpdate):
    if not check_permission(request.auth.user, "admin.theme.manage"):
        return 403, {"detail": "forbidden"}
    settings = _get_settings()
    settings.theme = payload.theme
    settings.save(update_fields=["theme"])
    return {"theme": settings.theme}


@router.get("/seo", response=SeoOut)
def get_seo(request):
    settings = _get_settings()
    return {
        "title": settings.seo_title,
        "description": settings.seo_description,
        "keywords": settings.seo_keywords,
        "og_image": settings.og_image,
    }


@router.post("/seo", response=SeoOut, auth=AuthBearer())
def update_seo(request, payload: SeoUpdate):
    if not check_permission(request.auth.user, "admin.seo.manage"):
        return 403, {"detail": "forbidden"}
    settings = _get_settings()
    if payload.title is not None:
        settings.seo_title = payload.title
    if payload.description is not None:
        settings.seo_description = payload.description
    if payload.keywords is not None:
        settings.seo_keywords = payload.keywords
    if payload.og_image is not None:
        settings.og_image = payload.og_image
    settings.save()
    return {
        "title": settings.seo_title,
        "description": settings.seo_description,
        "keywords": settings.seo_keywords,
        "og_image": settings.og_image,
    }
