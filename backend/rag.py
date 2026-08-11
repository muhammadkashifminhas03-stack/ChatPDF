from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def search_pdf(question):

    db = Chroma(
        persist_directory="vectorstore",
        embedding_function=embedding_model
    )

    results = db.similarity_search(question, k=3)

    if not results:
        return "I could not find anything related to your question in the PDF."

    context = ""

    for doc in results:
        context += doc.page_content + "\n\n"

    return context