import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

from utils.pdf_processor import process_pdf
from vector_db import create_vector_db, search


# =========================================================
# LOAD .ENV
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE, override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# =========================================================
# GROQ
# =========================================================

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY NOT FOUND")
    groq_client = None
else:
    print("GROQ API CONFIGURED")
    groq_client = Groq(api_key=GROQ_API_KEY)


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(title="ChatPDF")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "ChatPDF Backend Working",
        "groq": groq_client is not None
    }


# =========================================================
# UPLOAD PDF
# =========================================================

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    try:

        # Read PDF
        contents = await file.read()

        # Create uploads folder
        upload_dir = BASE_DIR / "uploads"
        upload_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # Save PDF
        pdf_path = upload_dir / file.filename

        with open(pdf_path, "wb") as f:
            f.write(contents)

        print("PDF saved:", file.filename)

        # Extract + chunk PDF
        chunks = process_pdf(
            str(pdf_path)
        )

        if not chunks:
            raise Exception(
                "No text could be extracted from this PDF."
            )

        print(
            "Chunks created:",
            len(chunks)
        )

        # Create FAISS database
        count = create_vector_db(
            chunks
        )

        print(
            "Vector database created:",
            count,
            "chunks"
        )

        return {
            "success": True,
            "message": "PDF uploaded successfully",
            "filename": file.filename,
            "chunks": count
        }

    except Exception as e:

        print(
            "UPLOAD ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# ASK PDF
# =========================================================

@app.post("/ask")
async def ask_pdf(data: dict):

    question = data.get(
        "question",
        ""
    ).strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question is required"
        )

    if groq_client is None:

        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not configured"
        )

    try:

        print()
        print("==============================")
        print("QUESTION:", question)
        print("==============================")


        # -------------------------------------------------
        # SEARCH VECTOR DATABASE
        # -------------------------------------------------

        results = search(
            question,
            k=5
        )


        if not results:

            return {
                "success": True,
                "answer": "I could not find this information in the PDF."
            }


        # -------------------------------------------------
        # BUILD PDF CONTEXT
        # -------------------------------------------------

        context_parts = []

        for result in results:

            context_parts.append(
                f"""
PAGE {result['page']}

{result['text']}
"""
            )

        context = "\n".join(
            context_parts
        )


        print(
            "Retrieved chunks:",
            len(results)
        )


        # -------------------------------------------------
        # GROQ PROMPT
        # -------------------------------------------------

        prompt = f"""
You are ChatPDF, an AI assistant that answers questions
about an uploaded PDF.

IMPORTANT:
Use ONLY the PDF content provided below.

PDF CONTENT:
================================

{context}

================================

USER QUESTION:
{question}

RULES:

1. Answer using only the PDF content.
2. Do not invent facts.
3. Do not use outside knowledge.
4. Give a clear and direct answer.
5. If the information is not present in the PDF, say:

"I could not find this information in the PDF."

6. If possible, mention the page number.

Answer the user now.
"""


        # -------------------------------------------------
        # CALL GROQ
        # -------------------------------------------------

        response = groq_client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are a PDF question answering assistant. "
                        "Answer strictly from the supplied PDF context."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.1,

            max_tokens=1000
        )


        answer = response.choices[0].message.content


        print(
            "ANSWER:",
            answer
        )


        # -------------------------------------------------
        # RETURN ANSWER
        # -------------------------------------------------

        return {
            "success": True,
            "answer": answer
        }


    except Exception as e:

        print(
            "ASK ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )