import fitz


def chunk_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)

    chunks = []

    for page_number, page in enumerate(doc):
        text = page.get_text("text").strip()

        if not text:
            continue

        # Split page text into manageable chunks
        words = text.split()

        chunk_size = 500

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size]).strip()

            if chunk:
                chunks.append(chunk)

    doc.close()

    return chunks