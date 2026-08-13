import { useState } from "react";

function App() {

  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [message, setMessage] = useState("");

  const uploadPDF = async () => {

    if (!file) {
      setMessage("Please select a PDF first");
      return;
    }

    setMessage("Uploading PDF...");
    setAnswer("");

    try {

      const formData = new FormData();

      formData.append(
        "file",
        file
      );

      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData
        }
      );

      const data =
        await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Upload failed"
        );
      }

      setMessage(
        `✅ PDF uploaded successfully. ${data.chunks} chunks created.`
      );

    } catch (error) {

      setMessage(
        `❌ ${error.message}`
      );
    }
  };


  const askQuestion = async () => {

    if (!question.trim()) {

      setAnswer(
        "Please enter a question."
      );

      return;
    }

    setAnswer("Thinking...");

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({
            question: question
          })
        }
      );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail || "Question failed"
        );
      }


      setAnswer(
        data.answer
      );

    } catch (error) {

      setAnswer(
        `❌ ${error.message}`
      );
    }
  };


  return (

    <div
      style={{
        maxWidth: "800px",
        margin: "40px auto",
        padding: "20px",
        fontFamily: "Arial"
      }}
    >

      <h1>📄 ChatPDF</h1>

      <p>
        Upload your PDF and ask questions
        about it.
      </p>


      <hr />


      <h2>Upload PDF</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(
            e.target.files[0]
          )
        }
      />

      <br />
      <br />

      <button
        onClick={uploadPDF}
      >
        Upload PDF
      </button>


      <p>
        {message}
      </p>


      <hr />


      <h2>Ask Your PDF</h2>

      <textarea
        rows="5"
        style={{
          width: "100%",
          padding: "10px"
        }}
        value={question}
        onChange={(e) =>
          setQuestion(
            e.target.value
          )
        }
        placeholder="Ask something about your PDF..."
      />

      <br />
      <br />

      <button
        onClick={askQuestion}
      >
        Ask Question
      </button>


      <h2>Answer</h2>

      <div
        style={{
          background: "#f5f5f5",
          padding: "20px",
          minHeight: "100px",
          whiteSpace: "pre-wrap"
        }}
      >
        {answer ||
          "Your answer will appear here."}
      </div>

    </div>

  );
}

export default App;