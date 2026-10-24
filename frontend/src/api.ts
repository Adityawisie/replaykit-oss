const BASE = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${BASE}${path}`, { ...init, headers: { ...(init.body ? { 'Content-Type': 'application/json' } : {}), ...init.headers } });
  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`;
    try { const data = await response.json(); message = data.detail || message; } catch { /* response wasn't JSON */ }
    throw new Error(message);
  }
  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json')) return response.json() as Promise<T>;
  return response.text() as T;
}
export async function downloadReport(body: unknown, format: 'json'|'markdown') {
  const response = await fetch(`${BASE}/api/reports/export?format=${format}`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body) });
  if (!response.ok) { let message = 'Export failed'; try { message = (await response.json()).detail || message; } catch {} throw new Error(message); }
  const blob = await response.blob(); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = format === 'json' ? 'replaykit-evidence.json' : 'replaykit-evidence.md'; a.click(); URL.revokeObjectURL(url);
}
