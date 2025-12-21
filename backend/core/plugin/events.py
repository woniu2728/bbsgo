import logging
from typing import Dict, List, Callable, Any
from collections import defaultdict

logger = logging.getLogger(__name__)


class EventBus:
    """
    简单的事件总线实现
    - 同步调用
    - 不引入 Celery
    """

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable):
        """
        订阅事件

        Args:
            event_name: 事件名称
            handler: 事件处理函数
        """
        self._handlers[event_name].append(handler)
        logger.debug(f"事件处理函数已订阅: {event_name}")

    def emit(self, event_name: str, **kwargs: Any):
        """
        触发事件

        Args:
            event_name: 事件名称
            **kwargs: 事件参数
        """
        handlers = self._handlers.get(event_name, [])

        if not handlers:
            logger.debug(f"事件无订阅者: {event_name}")
            return

        logger.debug(f"触发事件: {event_name}，处理函数数量: {len(handlers)}")

        for handler in handlers:
            try:
                handler(**kwargs)
            except Exception as e:
                logger.error(f"事件处理函数执行失败: {event_name} - {handler.__name__} - {e}")

    def unsubscribe(self, event_name: str, handler: Callable) -> bool:
        """
        取消订阅事件

        Args:
            event_name: 事件名称
            handler: 事件处理函数

        Returns:
            是否成功取消订阅
        """
        if event_name in self._handlers and handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)
            return True
        return False

    def clear(self, event_name: str = None):
        """
        清除事件处理函数

        Args:
            event_name: 事件名称，如果为None则清除所有
        """
        if event_name:
            if event_name in self._handlers:
                self._handlers[event_name].clear()
        else:
            self._handlers.clear()


# 全局事件总线实例
event_bus = EventBus()

# 便捷函数
def subscribe(event_name: str, handler: Callable):
    """订阅事件"""
    return event_bus.subscribe(event_name, handler)


def emit(event_name: str, **kwargs: Any):
    """触发事件"""
    return event_bus.emit(event_name, **kwargs)