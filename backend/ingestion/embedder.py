from sentence_transformers import SentenceTransformer
from uuid import uuid4


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

        embedding = model.encode(
            chunk,
            normalize_embeddings=True
        )

        embeddings.append({
            "text": chunk,
            "embedding": embedding.tolist(),
            "document_id": document_id,
            "filename": filename,
            "chunk_index": str(uuid4()),
        })

    return embeddings