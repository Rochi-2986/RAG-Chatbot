import { useState } from "react";

function SourceCard({ source }) {

  const [show, setShow] = useState(false);

  return (

    <div className="source-card">

      <button
        className="source-badge"
        onClick={() => setShow(!show)}
      >
        📄 {source.file} • Page {source.page}
      </button>

      {show && (

        <div className="source-preview">

          <h4>Preview</h4>

          <p>{source.preview}</p>

        </div>

      )}

    </div>

  );

}

export default SourceCard;