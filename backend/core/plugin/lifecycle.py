import logging
from typing import Optional
from .registry import registry

logger = logging.getLogger(__name__)


def enable_plugin(name: str) -> bool:
    """
    启用插件

    Args:
        name: 插件名称

    Returns:
        bool: 操作是否成功
    """
    plugin = registry.get(name)
    if plugin is None:
        logger.error(f"未找到插件: {name}")
        return False

    plugin.enabled = True
    logger.info(f"插件已启用: {name}")
    return True


def disable_plugin(name: str) -> bool:
    """
    禁用插件

    Args:
        name: 插件名称

    Returns:
        bool: 操作是否成功
    """
    plugin = registry.get(name)
    if plugin is None:
        logger.error(f"未找到插件: {name}")
        return False

    plugin.enabled = False
    logger.info(f"插件已禁用: {name}")
    return True


def get_plugin_status(name: str) -> Optional[bool]:
    """
    获取插件状态

    Args:
        name: 插件名称

    Returns:
        bool: 插件是否启用，如果插件不存在返回None
    """
    plugin = registry.get(name)
    if plugin is None:
        return None
    return plugin.enabled