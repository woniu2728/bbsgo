export function createRouter(routes, onRender) {
  const compiled = routes.map((route) => {
    const keys = [];
    const pattern = route.path
      .replace(/\/:([^/]+)/g, (_, key) => {
        keys.push(key);
        return "/([^/]+)";
      })
      .replace(/\//g, "\\/");
    return {
      ...route,
      regex: new RegExp(`^${pattern}$`),
      keys,
    };
  });

  function match(path) {
    for (const route of compiled) {
      const match = route.regex.exec(path);
      if (match) {
        const params = {};
        route.keys.forEach((key, index) => {
          params[key] = match[index + 1];
        });
        return { route, params };
      }
    }
    return null;
  }

  function render() {
    const path = location.hash.replace("#", "") || "/";
    const matched = match(path);
    if (matched) {
      onRender(matched.route.render({ params: matched.params, path }));
      return;
    }
    onRender(`<div class="card"><h2>Not Found</h2><p class="muted">${path}</p></div>`);
  }

  window.addEventListener("hashchange", render);
  render();
}
