import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [uploadMessage, setUploadMessage] = useState("");

  // =========================
  // UPLOAD PDF
  // =========================
  const uploadPDF = async () => {
    if (!file) {
      alert("Please select a PDF first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploadMessage("Uploading PDF...");

      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();

      setUploadMessage(
        `✅ ${data.message} (${data.chunks} chunks)`
      );

    } catch (error) {
      console.error(error);
      setUploadMessage("❌ Backend connection failed");
    }
  };


  // =========================
  // ASK QUESTION
  // =========================
  const askQuestion = async () => {
    if (!question.trim()) {
      alert("Please enter a question");
      return;
    }

    try {
      setAnswer("Thinking...");

      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Question failed");
      }

      const data = await response.json();

      setAnswer(data.answer);

    } catch (error) {
      console.error(error);
      setAnswer("❌ Could not get answer from backend.");
    }
  };


  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#f5f5f5",
        padding: "40px 20px",
        fontFamily: "Arial, sans-serif",
      }}
    >

      <div
        style={{
          maxWidth: "750px",
          margin: "0 auto",
          backgroundColor: "white",
          padding: "40px",
          borderRadius: "12px",
          boxShadow: "0 4px 15px rgba(0,0,0,0.1)",
        }}
      >

        {/* TITLE */}
        <h1
          style={{
            textAlign: "center",
            marginBottom: "10px",
          }}
        >
          📄 ChatPDF
        </h1>

        <p
          style={{
            textAlign: "center",
            color: "#666",
          }}
        >
          Upload a PDF and ask questions about it
        </p>


        {/* =========================
            PDF UPLOAD
        ========================= */}

        <h2>1. Upload PDF</h2>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => {
            setFile(e.target.files[0]);
            setUploadMessage("");
          }}
        />

        <br />
        <br />

        {file && (
          <p>
            📎 Selected file: <b>{file.name}</b>
          </p>
        )}

        <button
          onClick={uploadPDF}
          style={{
            padding: "10px 20px",
            cursor: "pointer",
            border: "none",
            borderRadius: "6px",
            backgroundColor: "#222",
            color: "white",
            fontSize: "16px",
          }}
        >
          Upload PDF
        </button>

        {uploadMessage && (
          <p
            style={{
              marginTop: "15px",
              fontWeight: "bold",
            }}
          >
            {uploadMessage}
          </p>
        )}


        <hr
          style={{
            margin: "30px 0",
          }}
        />


        {/* =========================
            ASK QUESTION
        ========================= */}

        <h2>2. Ask Your PDF</h2>

        <textarea
          rows="5"
          placeholder="Ask something about your PDF..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{
            width: "100%",
            padding: "12px",
            boxSizing: "border-box",
            fontSize: "16px",
            borderRadius: "6px",
            border: "1px solid #ccc",
            resize: "vertical",
          }}
        />

        <br />
        <br />

        <button
          onClick={askQuestion}
          style={{
            padding: "10px 25px",
            cursor: "pointer",
            border: "none",
            borderRadius: "6px",
            backgroundColor: "#222",
            color: "white",
            fontSize: "16px",
          }}
        >
          Ask Question
        </button>


        {/* =========================
            ANSWER
        ========================= */}

        <h2 style={{ marginTop: "30px" }}>
          Answer
        </h2>

        <div
          style={{
            minHeight: "100px",
            padding: "15px",
            border: "1px solid #ddd",
            borderRadius: "6px",
            backgroundColor: "#fafafa",
            whiteSpace: "pre-wrap",
          }}
        >
          {answer || "Your answer will appear here..."}
        </div>

      </div>

    </div>
  );
}

export default App;