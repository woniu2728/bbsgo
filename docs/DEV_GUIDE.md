# 插件开发指南（面向新手）

本指南帮助新成员在 30 分钟内完成一个可用插件（包含 API、权限、前端 manifest）。

## 1. 创建插件骨架

```bash
python backend/manage.py create_plugin demo
```

生成结构如下：

```text
backend/plugins/demo/
├─ plugin.yaml
├─ plugin.py
├─ apps.py
├─ backend/
│  ├─ api.py
│  ├─ models.py
│  ├─ permissions.py
│  └─ hooks.py
├─ frontend/
│  ├─ manifest.json
│  ├─ routes.ts
│  └─ pages/DemoHome.tsx
└─ migrations/
```

## 2. 配置 plugin.yaml

主要字段说明：

```yaml
name: demo
version: 0.1.0
api_version: 1
entry: plugins.demo.plugin:Plugin
dependencies: []
mount:
  api_prefix: /demo
```

- `entry`：插件入口类
- `dependencies`：依赖的插件列表
- `mount.api_prefix`：API 默认挂载前缀

## 3. 编写 API

在 `backend/plugins/demo/backend/api.py` 中新增路由：

```python
from ninja import Router

router = Router()

@router.get("/ping")
def ping(request):
    return {"ok": True}
```

在 `plugin.py` 中挂载路由：

```python
from plugins.demo.backend.api import router

class Plugin:
    def on_enable(self, api):
        api.add_router(router, tags=["demo"])
```

启动后访问：`GET /api/demo/ping`

## 4. 权限控制

推荐使用 ABI 提供的权限装饰器：

```python
@router.post("/create")
@api.require_permission("demo.create")
def create_item(request):
    ...
```

> 注意：如果未配置权限数据，默认会返回 403。

## 5. 前端 manifest

编辑 `frontend/manifest.json`，用于前端路由与菜单：

```json
{
  "name": "demo",
  "routes": [{ "path": "/demo", "component": "DemoHome" }],
  "menu": { "id": "demo", "label": "Demo", "path": "/demo" }
}
```

## 6. 数据库迁移

```bash
python backend/manage.py makemigrations demo
python backend/manage.py migrate
```

## 7. 启停插件

```bash
POST /api/plugins/enable
{"name": "demo"}

POST /api/plugins/disable
{"name": "demo", "cascade": true}
```

## 8. 校验插件

```bash
python backend/manage.py validate_plugins
```

检查内容：
- plugin.yaml 合法性
- 依赖存在
- 入口 import 可用
- 前端 manifest JSON 合法
- API 前缀冲突

## 9. 样例：基于 demo 插件快速上手

最简路径：
1. `create_plugin demo`
2. 添加 `/ping` API
3. 运行 `validate_plugins`
4. 启动服务验证

---

如需更复杂功能（RBAC、事件、跨插件调用），请参考 `plugins/forum` 实现。

## 10. 管理后台权限提示

管理员接口默认要求以下权限（superuser 自动放行）：
- `admin.plugins.manage`
- `admin.forum.manage`
- `admin.theme.manage`
- `admin.seo.manage`


## Plugin System Updates
- Optional lifecycle hook: on_disable(self, api) for cleanup.
- PluginAPI now exposes unsubscribe(event_name, handler).
- ABI version is enforced (supported: 1). Unsupported versions fail validation and are skipped at runtime.
- validate_plugins checks frontend route path and menu id conflicts across plugins.
