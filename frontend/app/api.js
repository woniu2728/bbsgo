const BASE = "http://127.0.0.1:8000";

export function getToken() {
  return localStorage.getItem("admin_token") || "";
}

export function setToken(token) {
  localStorage.setItem("admin_token", token);
}

export async function apiFetch(path, options = {}) {
  const headers = options.headers || {};
  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  if (options.body && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }
  const response = await fetch(`${BASE}${path}`, {
    ...options,
    headers,
  });
  const data = await response.json().catch(() => ({}));
  return { response, data };
}

export function backendFetch(path, options = {}) {
  return fetch(`${BASE}${path}`, options);
}
