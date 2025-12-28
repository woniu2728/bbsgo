import { registerPlugin } from "./registry.js";
import { registerTheme } from "./theme.js";
import { backendFetch } from "../api.js";

async function loadFrontendModule(name) {
  try {
    const module = await import(`../../plugins/${name}/index.js`);
    if (module?.plugin) {
      registerPlugin(module.plugin);
    }
  } catch (err) {
    console.warn(`Plugin frontend not found: ${name}`, err);
  }
}

function registerManifestFallback(frontend) {
  if (!frontend) return;
  if (frontend.routes) {
    const routes = frontend.routes.map((item) => ({
      path: item.path,
      render: () =>
        `<div class="card"><h2>${item.component}</h2><p class="muted">该页面暂无前端实现。</p></div>`,
    }));
    registerPlugin({ name: frontend.name || "manifest", routes });
  }
  if (frontend.menu) {
    registerPlugin({ name: frontend.name || "manifest", menu: [frontend.menu] });
  }
}

export async function loadPlugins() {
  const response = await backendFetch("/api/plugins/manifests");
  const data = await response.json();
  const plugins = data.plugins || [];

  for (const plugin of plugins) {
    registerManifestFallback(plugin.frontend);
    await loadFrontendModule(plugin.name);
  }

  await loadFrontendModule("admin_console");
  await loadFrontendModule("themes/classic");
  await loadFrontendModule("themes/noir");

  registerTheme();
}
