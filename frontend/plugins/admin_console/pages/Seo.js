import { apiFetch } from "../../../app/api.js";

export function renderSeo() {
  requestAnimationFrame(async () => {
    const { data } = await apiFetch("/api/ui-shell/seo");
    if (data) {
      document.getElementById("seo-title").value = data.title || "";
      document.getElementById("seo-desc").value = data.description || "";
      document.getElementById("seo-keywords").value = data.keywords || "";
      document.getElementById("seo-og").value = data.og_image || "";
    }

    document.getElementById("save-seo").addEventListener("click", async () => {
      const payload = {
        title: document.getElementById("seo-title").value,
        description: document.getElementById("seo-desc").value,
        keywords: document.getElementById("seo-keywords").value,
        og_image: document.getElementById("seo-og").value,
      };
      await apiFetch("/api/ui-shell/seo", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      alert("已保存");
    });
  });

  return `
    <div class="grid">
      <div class="card">
        <h2>SEO 配置</h2>
        <p class="muted">配置站点标题、描述与 OG 信息。</p>
      </div>
      <div class="card grid">
        <input id="seo-title" class="input" placeholder="站点标题" />
        <textarea id="seo-desc" class="textarea" placeholder="站点描述"></textarea>
        <input id="seo-keywords" class="input" placeholder="关键词（逗号分隔）" />
        <input id="seo-og" class="input" placeholder="OG Image URL" />
        <button id="save-seo" class="button">保存</button>
      </div>
    </div>
  `;
}
