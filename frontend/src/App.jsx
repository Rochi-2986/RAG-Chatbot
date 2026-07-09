import { useState } from "react";
import UploadPDF from "./components/UploadPDF";
import ChatBox from "./components/ChatBox";
import "./App.css";

function App() {

  const [currentPdf, setCurrentPdf] = useState("");

  return (

    <div className="app">

      <h1 className="title">
        RAG Chatbot
      </h1>

      <div className="upload-section">

        <UploadPDF
          setCurrentPdf={setCurrentPdf}
        />

      </div>

      <p className="current-doc">

        Current Document:

        {" "}

        {currentPdf || "No PDF Uploaded"}

      </p>

      <ChatBox
        currentPdf={currentPdf}
      />

    </div>

  );

}

export default App;