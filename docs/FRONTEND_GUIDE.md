# 前端开发文档（含管理后台）

本项目前端为“插件运行时 + 主题插件 + 管理后台”的组合结构。

## 1. 启动方式

前端为静态文件，直接用静态服务器打开即可：

```bash
cd frontend
python -m http.server 5173
```

浏览器访问：
```
http://localhost:5173/#/
```

## 2. 运行时加载流程

1) 拉取 `/api/ui-shell/manifest` 作为基础菜单  
2) 拉取 `/api/plugins/manifests` 获取启用插件及其 frontend manifest  
3) 动态加载 `frontend/plugins/<plugin>/index.js`  
4) 聚合 routes + menu + theme  
5) 渲染 `#` 路由

## 3. 论坛插件前端结构

```
frontend/plugins/forum/
├─ index.js
└─ pages/
   ├─ ForumHome.js
   └─ PostDetail.js
```

路由：
- `/forum`：帖子列表
- `/forum/:id`：帖子详情

## 4. 主题插件

```
frontend/plugins/themes/
├─ classic/index.js
└─ noir/index.js
```

主题通过 `/api/ui-shell/theme` 获取与保存，可在管理后台切换。

## 5. 管理后台（Admin Console）

入口：`#/admin`

页面：
- `/admin/plugins`：插件启用/禁用
- `/admin/forums`：版块管理
- `/admin/themes`：主题切换
- `/admin/seo`：SEO 配置

使用方式：
1) 先通过后端登录接口获取 token
2) 在 `/admin` 首页粘贴并保存 token

## 6. 添加前端插件

1) 创建前端插件目录：
```
frontend/plugins/<name>/index.js
```

2) 添加插件入口：
```js
export const plugin = {
  name: "<name>",
  routes: [{ path: "/xxx", render: () => "<div>...</div>" }],
  menu: [{ id: "<name>", label: "Name", path: "/xxx" }],
};
```

3) 更新后端插件的 `frontend/manifest.json`，保证前后端对齐：
```json
{
  "name": "<name>",
  "routes": [{ "path": "/xxx", "component": "PageName" }],
  "menu": { "id": "<name>", "label": "Name", "path": "/xxx" }
}
```

## 7. 常见问题

- 看不到插件页面：确认插件已启用，且前端模块存在
- 403：确认 token 正确且用户有权限（或为 superuser）


## Plugin System Updates
- Frontend registry ignores conflicting routes, menu ids, or themes and logs a warning in console.
- Backend validation reports route/menu conflicts in plugin frontend manifests.
