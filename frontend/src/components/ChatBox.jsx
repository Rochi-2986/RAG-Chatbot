import { useState, useRef, useEffect } from "react";
import axios from "axios";

function ChatBox({ currentPdf }) {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesRef = useRef(null);
  useEffect(() => {

  if (messagesRef.current) {
    messagesRef.current.scrollTo({
  top: messagesRef.current.scrollHeight,
  behavior: "smooth"
});
  }

}, [messages, loading]);

  const askQuestion = async () => {

    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      text: question
    };

    setMessages(prev => [...prev, userMessage]);

    setLoading(true);

    try {

      const res = await axios.post(
        "http://localhost:8000/chat",
        {
          question
        }
      );

      const botMessage = {
        role: "bot",
        text: res.data.answer,
        sources: res.data.sources
      };

      setMessages(prev => [
        ...prev,
        botMessage
      ]);

    } catch (err) {

      setMessages(prev => [
        ...prev,
        {
          role: "bot",
          text: "Error connecting to server."
        }
      ]);

    } finally {

      setLoading(false);
    }

    setQuestion("");
  };

  return (
    <div className="chat-container">

      <div className="messages" ref={messagesRef}>

        {messages.map((msg, index) => (

          <div
            key={index}
            className={
              msg.role === "user"
                ? "user-message"
                : "bot-message"
            }
          >

            <div
              className={
                msg.role === "user"
                  ? "user-bubble"
                  : "bot-bubble"
              }
            >

              <p>{msg.text}</p>

              {msg.sources && (

                <div className="sources">

                  {msg.sources.map(page => (

                    <span
                      key={page}
                      className="source-badge"
                    >
                      Page {page}
                    </span>

                  ))}

                </div>

              )}

            </div>

          </div>

        ))}

        {loading && (
          <p className="loading">
            Thinking...
          </p>
        )}

      </div>

      {!currentPdf && (
        <p className="upload-warning">
          Upload a PDF first
        </p>
      )}

      <div className="input-container">

        <input
          className="input-box"
          type="text"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          disabled={!currentPdf}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              askQuestion();
            }
          }}
        />

        <button
          className="send-btn"
          onClick={askQuestion}
          disabled={!currentPdf || loading}
        >
          Send
        </button>

      </div>

    </div>
  );
}

export default ChatBox;