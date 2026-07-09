import { useState, useRef, useEffect } from "react";
import axios from "axios";
import SourceCard from "./SourceCard";

function ChatBox({ currentPdf }) {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const messagesRef = useRef(null);


  useEffect(() => {

    if (!currentPdf) {

      setMessages([]);

      return;

    }

    const saved = localStorage.getItem(currentPdf);

    if (saved) {

      setMessages(JSON.parse(saved));

    }

    else {

      setMessages([]);

    }

  }, [currentPdf]);


  useEffect(() => {

    if (!currentPdf) return;

    localStorage.setItem(
      currentPdf,
      JSON.stringify(messages)
    );

  }, [messages, currentPdf]);


  useEffect(() => {

    if (!messagesRef.current) return;

    messagesRef.current.scrollTo({

      top: messagesRef.current.scrollHeight,

      behavior: "smooth"

    });

  }, [messages, loading]);


  const clearChat = () => {

    if (!window.confirm("Clear this conversation?"))
      return;

    localStorage.removeItem(currentPdf);
    setMessages([]);

  };


  const askQuestion = async () => {

    if (!question.trim()) return;

    const userMessage = {

      role: "user",

      text: question

    };

    setMessages(prev => [...prev, userMessage]);

    setQuestion("");

    setLoading(true);

    try {

      const res = await axios.post(
    "http://localhost:8000/chat",
    {
        question,
        pdf: currentPdf
    }
);
 console.log(res.data);

      const botMessage = {

        role: "bot",

        text: res.data.answer,

        sources: res.data.sources

      };

      setMessages(prev => [

        ...prev,

        botMessage

      ]);

    }

    catch {

      setMessages(prev => [

        ...prev,

        {

          role: "bot",

          text: "❌ Error connecting to server."

        }

      ]);

    }

    finally {

      setLoading(false);

    }

  };


  return (

    <div className="chat-container">

      <div

        className="messages"

        ref={messagesRef}

      >

        {

          messages.map((msg, index) => {

            if (msg.role === "system") {

              return (

                <div

                  key={index}

                  className="system-message"

                >

                  {msg.text}

                </div>

              );

            }

            return (

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

                  {

                    msg.sources && (

                      <div className="sources">
  {msg.sources.map((source, i) => (
    <SourceCard
      key={i}
      source={source}
    />
  ))}
</div>

                    )

                  }

                </div>

              </div>

            );

          })

        }

        {

          loading &&

          <p className="loading">

             Thinking...

          </p>

        }

      </div>

      {

        !currentPdf &&

        <p className="upload-warning">

          Upload a PDF first

        </p>

      }

      <div className="input-container">

        <input

          className="input-box"

          value={question}

          type="text"

          placeholder="Ask a question..."

          disabled={!currentPdf}

          onChange={(e) =>

            setQuestion(e.target.value)

          }

          onKeyDown={(e) => {

            if (e.key === "Enter")

              askQuestion();

          }}

        />

        <button

          className="send-btn"

          onClick={askQuestion}

          disabled={!currentPdf || loading}

        >

          Send

        </button>

        <button

          className="clear-btn"

          onClick={clearChat}

          disabled={loading}

        >

          Clear Chat

        </button>

      </div>

    </div>

  );

}

export default ChatBox;