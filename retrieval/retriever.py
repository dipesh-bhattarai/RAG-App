from sentence_transformers import SentenceTransformer
from db.qdrant import client, COLLECTION_NAME

MODEL = "nomic-ai/nomic-embed-text-v1.5"
model = SentenceTransformer(MODEL, trust_remote_code=True)

def retrieve(query:str, limit:int = 5):
    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query = query_embedding,
        limit=limit,
    )

    chunks = []
        
    for point in results.points:
        chunks.append(
            {
                "text":point.payload["text"],
                "filename":point.payload["filename"],
                "document_id":point.payload["document_id"],
                "chunk_index":point.payload["chunk_index"],
            }
        )
    return chunks
    

