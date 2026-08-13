import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq


# Find backend folder
BASE_DIR = Path(__file__).resolve().parent

# Load backend/.env explicitly
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=True)


# Read Groq key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise Exception(
        f"GROQ_API_KEY is missing.\n"
        f"Expected .env here: {ENV_FILE}"
    )


# Groq client
client = Groq(api_key=GROQ_API_KEY)


def ask_groq(context, question):

    prompt = f"""
You are a ChatPDF assistant.

Answer the question ONLY using the PDF content provided below.

PDF CONTENT:
{context}

QUESTION:
{question}

Rules:
- Give an accurate answer.
- Do not invent information.
- If the answer is not available in the PDF, say:
"I could not find this information in the PDF."
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=1000
    )

    return response.choices[0].message.content