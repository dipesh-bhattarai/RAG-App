from db.qdrant import client, COLLECTION_NAME
from ingestion.embedder import get_model


def vector_search(query: str, limit: int = 5):

    model = get_model()

    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        with_payload=True,
    )

    chunks = []

    for point in results.points:
        chunks.append(
            {
                "text": point.payload["text"],
                "document_id": point.payload["document_id"],
                "filename": point.payload["filename"],
                "page": point.payload["page"],
                "chunk_index": point.payload["chunk_index"],
                "score": point.score,
            }
        )

    return chunks