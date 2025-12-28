import { getToken, setToken } from "../../../app/api.js";

export function renderAdminHome() {
  requestAnimationFrame(() => {
    const input = document.getElementById("admin-token");
    const saved = getToken();
    if (saved) input.value = saved;
    document.getElementById("save-token").addEventListener("click", () => {
      setToken(input.value.trim());
      alert("Token saved");
    });
  });

  return `
    <div class="grid">
      <div class="card">
        <h2>管理员后台</h2>
        <p class="muted">管理插件、版块、主题与 SEO 配置。</p>
      </div>
      <div class="card">
        <h3>认证 Token</h3>
        <p class="muted">粘贴登录后返回的 bearer token。</p>
        <div class="row">
          <input id="admin-token" class="input" placeholder="Bearer Token" />
          <button id="save-token" class="button">保存</button>
        </div>
      </div>
      <div class="card">
        <div class="grid">
          <a href="#/admin/plugins">插件管理</a>
          <a href="#/admin/forums">版块管理</a>
          <a href="#/admin/themes">主题切换</a>
          <a href="#/admin/seo">SEO 配置</a>
        </div>
      </div>
    </div>
  `;
}
