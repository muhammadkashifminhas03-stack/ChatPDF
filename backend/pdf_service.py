import os
from dotenv import load_dotenv

from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

load_dotenv()

embeddings = OpenAIEmbeddings()

db = None


async def upload_pdf(file):

    global db

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    pdf = PdfReader(file_path)

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.create_documents([text])

    db = FAISS.from_documents(
        docs,
        embeddings
    )

    return "PDF uploaded successfully."


def ask_question(question):

    global db

    if db is None:
        return "Please upload a PDF first."

    docs = db.similarity_search(question)

    context = ""

    for doc in docs:
        context += doc.page_content + "\n"

    llm = ChatOpenAI(
        temperature=0
    )

    prompt = f"""
Answer only using the information below.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content