import pymupdf


CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = " ".join(text.split())

    return text


def chunk_pdf(pdf_path: str):
    doc = pymupdf.open(pdf_path)

    chunks = []

    for page_number, page in enumerate(doc, start=1):

        text = page.get_text("text")

        text = clean_text(text)

        if not text:
            continue

        words = text.split()

        start = 0

        while start < len(words):

            end = start + CHUNK_SIZE

            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words).strip()

            if chunk_text:
                chunks.append(
                    {
                        "text": chunk_text,
                        "page": page_number,
                        "chunk_index": len(chunks)
                    }
                )

            if end >= len(words):
                break

            start = end - CHUNK_OVERLAP

    doc.close()

    return chunks