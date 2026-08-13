from pypdf import PdfReader


def process_pdf(file_path):

    reader = PdfReader(file_path)

    chunks = []

    chunk_size = 1000
    overlap = 200

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""
        text = text.strip()

        if not text:
            continue

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page_number
                })

            if end >= len(text):
                break

            start = end - overlap

    print("Chunks created:", len(chunks))

    return chunks