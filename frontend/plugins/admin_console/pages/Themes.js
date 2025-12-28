import { apiFetch } from "../../../app/api.js";
import { getRegistry } from "../../../app/kernel/registry.js";
import { getActiveTheme, setActiveTheme } from "../../../app/kernel/theme.js";

export function renderThemes() {
  requestAnimationFrame(async () => {
    const { themes } = getRegistry();
    const list = document.getElementById("theme-list");
    const current = getActiveTheme();
    list.innerHTML = Object.keys(themes)
      .map(
        (theme) => `
        <div class="card">
          <div class="row">
            <strong>${theme}</strong>
            ${theme === current ? '<span class="badge">active</span>' : ""}
          </div>
          <button class="button" data-theme="${theme}">切换</button>
        </div>
      `
      )
      .join("");

    list.addEventListener("click", async (event) => {
      const theme = event.target.dataset?.theme;
      if (!theme) return;
      setActiveTheme(theme);
      await apiFetch("/api/ui-shell/theme", {
        method: "POST",
        body: JSON.stringify({ theme }),
      });
      location.reload();
    });
  });

  return `
    <div class="grid">
      <div class="card">
        <h2>主题切换</h2>
        <p class="muted">当前主题由后台记录，可统一团队风格。</p>
      </div>
      <div id="theme-list" class="grid"></div>
    </div>
  `;
}
