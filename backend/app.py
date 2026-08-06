from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pdf_service import upload_pdf
from pdf_service import ask_question

app = FastAPI(title="ChatPDF API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "ChatPDF API Running"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Upload a PDF file.")

    result = await upload_pdf(file)

    return {
        "status": "success",
        "message": result
    }

@app.post("/chat")
async def chat(data: dict):

    question = data.get("question")

    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    answer = ask_question(question)

    return {
        "answer": answer
    }