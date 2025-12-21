from ninja import NinjaAPI, Schema
from typing import List
from .plugin.registry import registry

api = NinjaAPI()

class PluginListItem(Schema):
    """插件列表项"""
    name: str
    version: str
    enabled: bool


@api.get("/plugins", response=List[PluginListItem])
def list_plugins(request):
    """获取插件列表"""
    plugins = []
    for plugin in registry.list_plugins():
        plugins.append({
            "name": plugin.name,
            "version": plugin.version,
            "enabled": plugin.enabled
        })
    return plugins