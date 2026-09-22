from sentence_transformers import SentenceTransformer

MODEL = "nomic-ai/nomic-embed-text-v1.5"

model = SentenceTransformer(MODEL, trust_remote_code=True)

def embed_text(chunks):
    embeddings = []

    for chunk in chunks:
        embedding = model.encode(
            chunk.text,
            normalize_embeddings=True
        )

        embeddings.append({
            "text": chunk.text,
            "embedding": embedding.tolist()
        })

    return embeddings
    