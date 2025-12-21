import os
import yaml
import logging
from pathlib import Path
from typing import List, Dict, Optional
from .registry import PluginMeta, registry

logger = logging.getLogger(__name__)

# 获取插件目录的绝对路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PLUGINS_DIR = BASE_DIR / "plugins"


def discover_plugins() -> List[str]:
    """扫描backend/plugins目录，返回包含plugin.yaml的插件路径列表"""
    plugin_paths = []
    plugins_dir = Path(PLUGINS_DIR)

    if not plugins_dir.exists():
        logger.warning(f"插件目录不存在: {PLUGINS_DIR}")
        return plugin_paths

    # 扫描plugins目录下的所有子目录
    for item in plugins_dir.iterdir():
        if item.is_dir() and (item / "plugin.yaml").exists():
            plugin_paths.append(str(item))

    return plugin_paths


def load_plugin_yaml(plugin_path: str) -> Optional[Dict]:
    """
    解析plugin.yaml文件，返回插件配置
    如果schema不合法，返回None并记录日志
    """
    plugin_file = Path(plugin_path) / "plugin.yaml"

    try:
        with open(plugin_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # 验证基本schema
        if not isinstance(config, dict):
            logger.error(f"插件配置文件格式错误（非dict）: {plugin_file}")
            return None

        if 'name' not in config or 'version' not in config:
            logger.error(f"插件配置文件缺少必需字段（name或version）: {plugin_file}")
            return None

        return config
    except yaml.YAMLError as e:
        logger.error(f"插件YAML解析错误: {plugin_file} - {e}")
        return None
    except IOError as e:
        logger.error(f"读取插件配置文件失败: {plugin_file} - {e}")
        return None


def load_plugins():
    """
    加载所有插件（Phase 1只注册元数据，不加载插件代码）
    按照强制顺序：
    1. 解析 plugin.yaml
    2. 构造 PluginMeta（enabled=False）
    3. 注册到 PluginRegistry
    """
    plugin_paths = discover_plugins()

    for plugin_path in plugin_paths:
        config = load_plugin_yaml(plugin_path)

        if config is None:
            # 日志已在load_plugin_yaml中记录，跳过
            continue

        # 构造插件元数据
        plugin_meta = PluginMeta(
            name=config['name'],
            version=config['version'],
            path=plugin_path,
            enabled=False  # Phase 1中所有插件默认禁用
        )

        # 注册到注册表
        registry.register(plugin_meta)
        logger.info(f"插件已注册: {plugin_meta.name} v{plugin_meta.version}")

    logger.info(f"插件加载完成，共加载 {len(registry.list_plugins())} 个插件")