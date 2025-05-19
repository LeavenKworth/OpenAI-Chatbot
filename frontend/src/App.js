import React, { useState, useEffect, useRef } from "react";

const API_URL = "http://localhost:5265/chat";

export default function ChatApp() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! How can I help you today?" },
  ]);
  const [input, setInput] = useState("");
  const [error, setError] = useState(null); 
  const [loading, setLoading] = useState(false); 
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    const trimmedInput = input.trim();
    if (!trimmedInput) return;

    setError(null); 
    setLoading(true);

    
    setMessages((prev) => [...prev, { sender: "user", text: trimmedInput }]);
    setInput("");

    try {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: trimmedInput }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    console.error("API responded with error:", res.status, errorText);
    setError(`Server error: ${res.status} - ${errorText}`);
    setMessages((prev) => [
      ...prev,
      { sender: "bot", text: `Error from server: ${res.status}` },
    ]);
    setLoading(false);
    return;
  }

  const data = await res.json();
  console.log("API response data:", data);

  const botReply = data.response?.output || "No response from server.";

  setMessages((prev) => [...prev, { sender: "bot", text: botReply }]);
} catch (err) {
  console.error("Fetch error:", err);
  setError("Unable to connect to server.");
  setMessages((prev) => [
    ...prev,
    { sender: "bot", text: "Unable to connect to server." },
  ]);
} finally {
  setLoading(false);
}

  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div style={styles.container}>
      <div style={styles.chatWindow}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              ...styles.message,
              alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              backgroundColor: msg.sender === "user" ? "#4caf50" : "#eee",
              color: msg.sender === "user" ? "white" : "black",
            }}
          >
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div style={styles.inputArea}>
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          style={styles.input}
          disabled={loading}
          autoFocus
        />
        <button onClick={sendMessage} style={styles.button} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>

      {error && (
        <div style={styles.errorBox}>
          <strong>Error:</strong> {error}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 600,
    margin: "50px auto",
    border: "1px solid #ccc",
    borderRadius: 8,
    display: "flex",
    flexDirection: "column",
    height: "80vh",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
  },
  chatWindow: {
    flexGrow: 1,
    padding: 15,
    display: "flex",
    flexDirection: "column",
    gap: 10,
    overflowY: "auto",
    backgroundColor: "#fafafa",
    borderRadius: "8px 8px 0 0",
  },
  message: {
    maxWidth: "70%",
    padding: 12,
    borderRadius: 15,
    wordBreak: "break-word",
    fontSize: 16,
  },
  inputArea: {
    display: "flex",
    borderTop: "1px solid #ccc",
  },
  input: {
    flexGrow: 1,
    padding: 15,
    fontSize: 16,
    border: "none",
    outline: "none",
    borderRadius: "0 0 0 8px",
  },
  button: {
    backgroundColor: "#4caf50",
    color: "white",
    border: "none",
    padding: "0 20px",
    cursor: "pointer",
    fontSize: 16,
    borderRadius: "0 0 8px 0",
    transition: "background-color 0.3s ease",
  },
  errorBox: {
    marginTop: 10,
    padding: 10,
    backgroundColor: "#f8d7da",
    color: "#721c24",
    borderRadius: 5,
    border: "1px solid #f5c6cb",
  },
};
