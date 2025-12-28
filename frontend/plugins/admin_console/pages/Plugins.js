import { apiFetch } from "../../../app/api.js";

function renderRows(plugins) {
  return plugins
    .map(
      (plugin) => `
      <div class="card">
        <div class="row">
          <strong>${plugin.name}</strong>
          <span class="badge">${plugin.enabled ? "enabled" : "disabled"}</span>
        </div>
        <p class="muted">${plugin.description || "No description"}</p>
        <div class="row">
          <button class="button" data-action="enable" data-name="${plugin.name}">启用</button>
          <button class="button secondary" data-action="disable" data-name="${plugin.name}">禁用</button>
        </div>
      </div>
    `
    )
    .join("");
}

export function renderPlugins() {
  requestAnimationFrame(async () => {
    const container = document.getElementById("plugin-list");
    const { data } = await apiFetch("/api/plugins");
    const plugins = data.plugins || [];
    container.innerHTML = renderRows(plugins);

    container.addEventListener("click", async (event) => {
      const target = event.target;
      if (!target.dataset?.action) return;
      const name = target.dataset.name;
      const action = target.dataset.action;
      const body = JSON.stringify({ name, cascade: true });
      await apiFetch(`/api/plugins/${action}`, { method: "POST", body });
      const refreshed = await apiFetch("/api/plugins");
      container.innerHTML = renderRows(refreshed.data.plugins || []);
    });
  });

  return `
    <div class="grid">
      <div class="card">
        <h2>插件管理</h2>
        <p class="muted">启用/禁用插件并查看状态。</p>
      </div>
      <div id="plugin-list" class="grid"></div>
    </div>
  `;
}
