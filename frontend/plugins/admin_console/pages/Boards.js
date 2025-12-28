import { apiFetch } from "../../../app/api.js";

function renderBoard(board) {
  return `
    <div class="card">
      <div class="grid">
        <div class="row">
          <input class="input" data-field="name" data-id="${board.id}" value="${board.name}" />
          <input class="input" data-field="slug" data-id="${board.id}" value="${board.slug}" />
        </div>
        <div class="row">
          <input class="input" data-field="order" data-id="${board.id}" value="${board.order}" />
          <label class="row">
            <input type="checkbox" data-field="is_active" data-id="${board.id}" ${board.is_active ? "checked" : ""} />
            <span class="muted">启用</span>
          </label>
        </div>
        <textarea class="textarea" data-field="description" data-id="${board.id}">${board.description || ""}</textarea>
        <div class="row">
          <button class="button" data-action="save" data-id="${board.id}">保存</button>
          <button class="button secondary" data-action="delete" data-id="${board.id}">删除</button>
        </div>
      </div>
    </div>
  `;
}

export function renderBoards() {
  requestAnimationFrame(async () => {
    const list = document.getElementById("board-list");
    const { data } = await apiFetch("/api/forum/boards/all");
    const boards = data || [];
    list.innerHTML = boards.map(renderBoard).join("");

    document.getElementById("create-board").addEventListener("click", async () => {
      const name = document.getElementById("board-name").value.trim();
      const slug = document.getElementById("board-slug").value.trim();
      if (!name || !slug) return;
      await apiFetch("/api/forum/boards", {
        method: "POST",
        body: JSON.stringify({ name, slug }),
      });
      location.reload();
    });

    list.addEventListener("click", async (event) => {
      const target = event.target;
      const action = target.dataset?.action;
      if (!action) return;
      const id = target.dataset.id;
      if (action === "delete") {
        await apiFetch(`/api/forum/boards/${id}`, { method: "DELETE" });
        location.reload();
        return;
      }
      if (action === "save") {
        const fields = list.querySelectorAll(`[data-id="${id}"]`);
        const payload = {};
        fields.forEach((field) => {
          const key = field.dataset.field;
          if (field.type === "checkbox") {
            payload[key] = field.checked;
          } else {
            payload[key] = field.value;
          }
        });
        payload.order = Number(payload.order || 0);
        await apiFetch(`/api/forum/boards/${id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
        location.reload();
      }
    });
  });

  return `
    <div class="grid">
      <div class="card">
        <h2>版块管理</h2>
        <div class="row">
          <input id="board-name" class="input" placeholder="版块名称" />
          <input id="board-slug" class="input" placeholder="slug" />
          <button id="create-board" class="button">新增</button>
        </div>
      </div>
      <div id="board-list" class="grid"></div>
    </div>
  `;
}
