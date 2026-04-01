const API_BASE = import.meta.env.VITE_API_BASE || "https://utz-consumer-intelligence.onrender.com";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }

  return response.json();
}

export const api = {
  getSummary: () => request('/insights/summary'),
  getQueries: ({ search = '', channel = 'all' } = {}) =>
    request(`/queries?search=${encodeURIComponent(search)}&channel=${encodeURIComponent(channel)}`),
  getGaps: () => request('/insights/gaps'),
  getActions: () => request('/actions/recommendations'),
  askCopilot: (question) =>
    request('/copilot/ask', {
      method: 'POST',
      body: JSON.stringify({ question, context_mode: 'executive' }),
    }),
};
