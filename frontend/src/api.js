const API = "http://localhost:8000";

export async function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);
  const resp = await fetch(`${API}/upload`, { method: "POST", body: form });
  return resp.json();
}

export async function postText(endpoint, data) {
  const resp = await fetch(`${API}/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return resp.json();
}
