import { useState } from "react";
import axios from "axios";

function UploadPDF({ 
  setCurrentPdf,
}) {

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadFile = async () => {

    if (!file) {
      alert("Please select a PDF");
      return;
    }

    try {

      setLoading(true);

      const formData = new FormData();

      formData.append(
        "file",
        file
      );

      const res = await axios.post(
        "http://localhost:8000/upload",
        formData
      );

      setCurrentPdf(
        res.data.filename
      );
     

      alert(
        `${res.data.message}\n\nChunks: ${res.data.chunks}`
      );

    } catch (err) {

      console.error(err);

      alert(err.message);

    } finally {

      setLoading(false);
    }
  };

  return (
    <div className="upload-section">

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <button
        onClick={uploadFile}
        disabled={loading}
      >
        {loading
          ? "Uploading..."
          : "Upload PDF"}
      </button>

    </div>
  );
}

export default UploadPDF;