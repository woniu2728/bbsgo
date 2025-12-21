"""
插件开发SDK - 为插件提供统一的API接口
所有插件必须通过此SDK访问系统能力
"""
from typing import Any, Dict, Optional, Type, Callable, List
from django.http import JsonResponse
from ninja import Router
from .registry import plugin_registry
from .events import event_bus
from .lifecycle import get_plugin_lifecycle_manager


class PluginAPI:
    """插件API接口类 - 插件访问系统能力的唯一入口"""

    def __init__(self, plugin_name: str):
        """
        初始化插件API

        Args:
            plugin_name: 插件名称
        """
        self.plugin_name = plugin_name
        self._routers: List[Router] = []

    def register_router(self, router: Router) -> None:
        """
        注册Ninja路由器

        Args:
            router: Ninja Router实例
        """
        self._routers.append(router)

        # 获取插件元数据
        plugin_meta = plugin_registry.get_plugin(self.plugin_name)
        if plugin_meta:
            # 将路由器存储在插件元数据中
            if not hasattr(plugin_meta, 'routers'):
                plugin_meta.routers = []
            plugin_meta.routers.append(router)

    def get_event_bus(self):
        """
        获取事件总线实例

        Returns:
            EventBus实例
        """
        return event_bus

    def emit_event(self, event_name: str, **kwargs) -> None:
        """
        触发事件

        Args:
            event_name: 事件名称
            **kwargs: 事件参数
        """
        event_bus.emit(event_name, **kwargs)

    def subscribe_event(self, event_name: str, handler: Callable) -> None:
        """
        订阅事件

        Args:
            event_name: 事件名称
            handler: 事件处理函数
        """
        event_bus.subscribe(event_name, handler)

    def unsubscribe_event(self, event_name: str, handler: Callable) -> None:
        """
        取消订阅事件

        Args:
            event_name: 事件名称
            handler: 事件处理函数
        """
        event_bus.unsubscribe(event_name, handler)

    def get_plugin_config(self) -> Dict[str, Any]:
        """
        获取插件配置

        Returns:
            插件配置字典
        """
        plugin_meta = plugin_registry.get_plugin(self.plugin_name)
        if plugin_meta and hasattr(plugin_meta, 'config'):
            return plugin_meta.config
        return {}

    def get_plugin_info(self) -> Optional[Dict[str, Any]]:
        """
        获取插件信息

        Returns:
            插件信息字典，包含名称、版本、路径等
        """
        plugin_meta = plugin_registry.get_plugin(self.plugin_name)
        if plugin_meta:
            return {
                'name': plugin_meta.name,
                'version': plugin_meta.version,
                'path': plugin_meta.path,
                'enabled': plugin_meta.enabled
            }
        return None

    def is_plugin_enabled(self, plugin_name: str) -> bool:
        """
        检查插件是否启用

        Args:
            plugin_name: 插件名称

        Returns:
            插件是否启用
        """
        plugin_meta = plugin_registry.get_plugin(plugin_name)
        return plugin_meta.enabled if plugin_meta else False

    def get_all_plugins(self) -> List[Dict[str, Any]]:
        """
        获取所有插件信息

        Returns:
            插件信息列表
        """
        plugins = []
        for plugin_meta in plugin_registry.list_plugins():
            plugins.append({
                'name': plugin_meta.name,
                'version': plugin_meta.version,
                'path': plugin_meta.path,
                'enabled': plugin_meta.enabled
            })
        return plugins