export function renderMenu(items) {
  const current = location.hash.replace("#", "") || "/";
  return items
    .map(
      (item) =>
        `<a href="#${item.path}" class="${current === item.path ? "active" : ""}">${item.label}</a>`
    )
    .join("");
}
