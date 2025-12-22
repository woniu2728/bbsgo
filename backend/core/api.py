"""
Core API - 插件系统集成核心接口
职责：提供插件路由挂载等基础功能，不包含插件管理逻辑
"""
from ninja import NinjaAPI

# 核心API实例
api = NinjaAPI(title="Forum Core API", version="1.0.0")