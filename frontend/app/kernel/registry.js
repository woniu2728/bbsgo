const registry = {
  routes: [],
  menus: [],
  themes: {},
};

const seen = {
  routes: new Map(),
  menus: new Map(),
  themes: new Map(),
};

export function registerPlugin(plugin) {
  const pluginName = plugin?.name || "unknown";
  if (plugin.routes) {
    for (const route of plugin.routes) {
      const path = route?.path;
      if (!path) {
        continue;
      }
      const owner = seen.routes.get(path);
      if (owner) {
        console.warn(`Route conflict: ${path} from ${pluginName} ignored (owned by ${owner})`);
        continue;
      }
      seen.routes.set(path, pluginName);
      registry.routes.push(route);
    }
  }
  if (plugin.menu) {
    for (const item of plugin.menu) {
      const menuId = item?.id;
      if (!menuId) {
        registry.menus.push(item);
        continue;
      }
      const owner = seen.menus.get(menuId);
      if (owner) {
        console.warn(`Menu id conflict: ${menuId} from ${pluginName} ignored (owned by ${owner})`);
        continue;
      }
      seen.menus.set(menuId, pluginName);
      registry.menus.push(item);
    }
  }
  if (plugin.theme) {
    const themeName = plugin.theme?.name;
    if (!themeName) {
      return;
    }
    const owner = seen.themes.get(themeName);
    if (owner) {
      console.warn(`Theme conflict: ${themeName} from ${pluginName} ignored (owned by ${owner})`);
      return;
    }
    seen.themes.set(themeName, pluginName);
    registry.themes[themeName] = plugin.theme;
  }
}

export function getRegistry() {
  return registry;
}
