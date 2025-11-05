import React, { useState } from "react";
import { sendMessage } from "./api";

function App() {
  const [input, setInput] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    try {
      const data = await sendMessage(input, conversationId);
      setReply(data.response);
      if (data.conversation_id) setConversationId(data.conversation_id);
    } catch (error) {
      alert(`Error: ${error.message}`);
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ color: "#0066cc" }}>🎓 AskEd Chatbot</h1>
<p>Hello! I'm AskEd 🤖 — your virtual assistant for university student services.</p>

      <form onSubmit={handleSubmit} style={{ marginTop: "20px" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me something..."
          style={{
            width: "70%",
            padding: "10px",
            fontSize: "16px",
            borderRadius: "8px",
            border: "1px solid #ccc",
          }}
        />
        <button
          type="submit"
          disabled={loading || !input}
          style={{
            marginLeft: "10px",
            padding: "10px 16px",
            fontSize: "16px",
            borderRadius: "8px",
            backgroundColor: loading ? "#ccc" : "#2E8B57",
            color: "#fff",
            border: "none",
            cursor: "pointer",
          }}
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </form>

      {reply && (
        <div
          style={{
            marginTop: "30px",
            padding: "15px",
            backgroundColor: "#f6f6f6",
            borderRadius: "8px",
            maxWidth: "70%",
          }}
        >
          <strong>Response:</strong>
          <p>{reply}</p>
        </div>
      )}
    </div>
  );
}

export default App;
