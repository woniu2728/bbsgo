export function renderLayout({ menuHtml, contentHtml }) {
  return `
    <div class="app-shell">
      <aside class="sidebar">
        <div class="brand">Forum Kernel</div>
        <nav class="menu">${menuHtml}</nav>
      </aside>
      <main class="content">${contentHtml}</main>
    </div>
  `;
}
