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
