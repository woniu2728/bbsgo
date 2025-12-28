import { getRegistry } from "./registry.js";
import { backendFetch } from "../api.js";

let activeTheme = "classic";

function applyTokens(tokens) {
  const root = document.documentElement;
  Object.entries(tokens).forEach(([key, value]) => {
    root.style.setProperty(key, value);
  });
}

export async function registerTheme() {
  try {
    const response = await backendFetch("/api/ui-shell/theme");
    const data = await response.json();
    if (data?.theme) {
      activeTheme = data.theme;
    }
  } catch (err) {
    console.warn("Theme fetch failed", err);
  }

  const { themes } = getRegistry();
  const theme = themes[activeTheme] || themes.classic;
  if (theme?.tokens) {
    applyTokens(theme.tokens);
  }
}

export function setActiveTheme(name) {
  activeTheme = name;
  const { themes } = getRegistry();
  const theme = themes[activeTheme];
  if (theme?.tokens) {
    applyTokens(theme.tokens);
  }
}

export function getActiveTheme() {
  return activeTheme;
}
