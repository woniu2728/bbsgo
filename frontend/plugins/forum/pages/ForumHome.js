const API_BASE = "http://127.0.0.1:8000";

function escapeHtml(text) {
  return String(text || "").replace(/[&<>"']/g, (match) => {
    const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
    return map[match];
  });
}

async function loadPosts(boardId) {
  const query = boardId ? `?board_id=${boardId}` : "";
  const response = await fetch(`${API_BASE}/api/forum/posts${query}`);
  return response.json();
}

async function loadBoards() {
  const response = await fetch(`${API_BASE}/api/forum/boards`);
  return response.json();
}

export function renderForumHome() {
  requestAnimationFrame(async () => {
    const boardSelect = document.getElementById("board-filter");
    const boardData = await loadBoards();
    const boards = Array.isArray(boardData) ? boardData : [];
    boardSelect.innerHTML =
      '<option value="">全部版块</option>' +
      boards.map((board) => `<option value="${board.id}">${escapeHtml(board.name)}</option>`).join("");

    const list = document.getElementById("post-list");
    const renderList = async (boardId) => {
      const posts = await loadPosts(boardId);
      list.innerHTML = posts
        .map(
          (post) => `
            <div class="card">
              <div class="row">
                <span class="badge">#${post.id}</span>
                <a href="#/forum/${post.id}">${escapeHtml(post.title)}</a>
              </div>
              <p class="muted">${escapeHtml(post.content).slice(0, 120)}...</p>
            </div>
          `
        )
        .join("");
    };

    boardSelect.addEventListener("change", (event) => {
      renderList(event.target.value || null);
    });

    renderList();
  });

  return `
    <div class="grid">
      <div class="hero">
        <h1>论坛</h1>
        <p class="muted">最新帖子与讨论内容展示。</p>
        <div class="row" style="margin-top: 12px;">
          <label class="muted">筛选版块</label>
          <select id="board-filter" class="select" style="max-width: 220px;"></select>
        </div>
      </div>
      <div id="post-list" class="grid"></div>
    </div>
  `;
}
