const API_BASE = "http://127.0.0.1:8000";

function escapeHtml(text) {
  return String(text || "").replace(/[&<>"']/g, (match) => {
    const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
    return map[match];
  });
}

async function loadPost(id) {
  const response = await fetch(`${API_BASE}/api/forum/posts/${id}`);
  return response.json();
}

async function loadComments(id) {
  const response = await fetch(`${API_BASE}/api/forum/comments?post_id=${id}`);
  return response.json();
}

export function renderPostDetail({ params }) {
  const postId = params.id;
  requestAnimationFrame(async () => {
    const post = await loadPost(postId);
    const comments = await loadComments(postId);
    const container = document.getElementById("post-detail");
    const commentHtml = comments
      .map(
        (comment) => `
        <div class="card">
          <p>${escapeHtml(comment.content)}</p>
          <p class="muted">#${comment.id}</p>
        </div>`
      )
      .join("");
    container.innerHTML = `
      <div class="card">
        <div class="row">
          <span class="badge">#${post.id}</span>
          <h2>${escapeHtml(post.title)}</h2>
        </div>
        <p>${escapeHtml(post.content)}</p>
      </div>
      <div class="grid" style="margin-top: 18px;">
        <h3>评论</h3>
        ${commentHtml || '<p class="muted">暂无评论</p>'}
      </div>
    `;
  });

  return `<div id="post-detail" class="grid"></div>`;
}
