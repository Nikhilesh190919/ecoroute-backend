const backendUrl = process.env.REACT_APP_BACKEND_URL;

export async function sendMessage(message, conversationId = null) {
  const res = await fetch(`${backendUrl}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Backend error ${res.status}: ${text}`);
  }

  return res.json(); // Expected: { response, conversation_id, sources }
}

export async function getAnalytics() {
  const res = await fetch(`${backendUrl}/api/analytics`);
  if (!res.ok) throw new Error(`Analytics failed: ${res.status}`);
  return res.json();
}
