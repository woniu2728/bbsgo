import { loadPlugins } from "./loader.js";
import { getRegistry, registerPlugin } from "./registry.js";
import { createRouter } from "../router.js";
import { backendFetch } from "../api.js";
import { renderLayout } from "../shell/layout.js";
import { renderMenu } from "../shell/menu.js";

function renderApp(contentHtml) {
  const app = document.getElementById("app");
  const { menus } = getRegistry();
  const menuHtml = renderMenu(menus);
  app.innerHTML = renderLayout({ menuHtml, contentHtml });
}

async function loadBaseMenus() {
  try {
    const response = await backendFetch("/api/ui-shell/manifest");
    const data = await response.json();
    if (data?.menus) {
      registerPlugin({ name: "ui-shell", menu: data.menus });
    }
  } catch (err) {
    console.warn("Failed to load ui-shell manifest", err);
  }
}

function registerBaseRoutes() {
  registerPlugin({
    name: "core",
    routes: [
      {
        path: "/",
        render: () =>
          `<div class="hero"><h1>欢迎来到论坛</h1><p class="muted">插件化内核已启动，开始探索吧。</p></div>`,
      },
    ],
  });
}

export async function boot() {
  registerBaseRoutes();
  await loadBaseMenus();
  await loadPlugins();
  const { routes } = getRegistry();
  createRouter(routes, renderApp);
}
