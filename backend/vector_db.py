import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# =========================================================
# EMBEDDING MODEL
# =========================================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# =========================================================
# VECTOR DATABASE
# =========================================================

VECTORSTORE = os.path.join(
    os.path.dirname(__file__),
    "vectorstore"
)

db = None
stored_chunks = []


# =========================================================
# CREATE VECTOR DATABASE
# =========================================================

def create_vector_db(chunks):

    global db
    global stored_chunks

    if not chunks:
        raise ValueError("No chunks were created from the PDF.")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print("Creating embeddings for", len(texts), "chunks...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    db = faiss.IndexFlatIP(dimension)

    db.add(embeddings)

    stored_chunks = chunks

    os.makedirs(
        VECTORSTORE,
        exist_ok=True
    )

    faiss.write_index(
        db,
        os.path.join(
            VECTORSTORE,
            "index.faiss"
        )
    )

    print(
        "Vector database created:",
        len(stored_chunks),
        "chunks"
    )

    return len(stored_chunks)


# =========================================================
# SEARCH PDF
# =========================================================

def search(question, k=5):

    global db
    global stored_chunks

    if db is None:
        print("ERROR: Vector database is empty.")
        return []

    if not stored_chunks:
        print("ERROR: No stored chunks.")
        return []

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    question_embedding = np.asarray(
        question_embedding,
        dtype="float32"
    )

    number_to_search = min(
        k,
        len(stored_chunks)
    )

    scores, indexes = db.search(
        question_embedding,
        number_to_search
    )

    results = []

    for score, index in zip(
        scores[0],
        indexes[0]
    ):

        if index < 0:
            continue

        chunk = stored_chunks[index]

        results.append({
            "text": chunk["text"],
            "page": chunk.get("page", "Unknown"),
            "score": float(score)
        })

    print("\nSEARCH QUESTION:")
    print(question)

    print("\nRETRIEVED CHUNKS:")

    for result in results:
        print(
            "Page:",
            result["page"],
            "| Score:",
            round(result["score"], 4)
        )

    return results