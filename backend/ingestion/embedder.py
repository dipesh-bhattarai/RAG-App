from sentence_transformers import SentenceTransformer


MODEL = "nomic-ai/nomic-embed-text-v1.5"

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer(
            MODEL,
            trust_remote_code=True
        )

    return model


def embed_text(chunks, document_id, filename):

    model = get_model()

    embeddings = []

    for chunk in chunks:

        text = chunk["text"]

        embedding = model.encode(
            text,
            normalize_embeddings=True
        )

        embeddings.append(
            {
                "text": text,
                "embedding": embedding.tolist(),
                "document_id": document_id,
                "filename": filename,
                "page": chunk["page"],
                "chunk_index": chunk["chunk_index"]
            }
        )

    return embeddings