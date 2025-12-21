class PluginMeta:
    def __init__(self, name: str, version: str, path: str, enabled: bool = False):
        self.name = name
        self.version = version
        self.path = path
        self.enabled = enabled

class PluginRegistry:
    def __init__(self):
        self._plugins = {}

    def register(self, plugin_meta: PluginMeta):
        """注册插件元数据"""
        self._plugins[plugin_meta.name] = plugin_meta

    def list_plugins(self):
        """返回所有插件的列表"""
        return list(self._plugins.values())

    def get(self, name: str) -> PluginMeta | None:
        """根据名称获取插件"""
        return self._plugins.get(name)

    def remove(self, name: str) -> bool:
        """移除插件"""
        if name in self._plugins:
            del self._plugins[name]
            return True
        return False

# 全局插件注册表实例
registry = PluginRegistry()