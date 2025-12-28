from ninja import Schema


class MenuItem(Schema):
    id: str
    label: str
    path: str


class LayoutSpec(Schema):
    name: str
    regions: list[str]


class UiShellManifest(Schema):
    menus: list[MenuItem]
    layout: LayoutSpec


class ThemeOut(Schema):
    theme: str


class ThemeUpdate(Schema):
    theme: str


class SeoOut(Schema):
    title: str
    description: str
    keywords: str
    og_image: str


class SeoUpdate(Schema):
    title: str | None = None
    description: str | None = None
    keywords: str | None = None
    og_image: str | None = None
