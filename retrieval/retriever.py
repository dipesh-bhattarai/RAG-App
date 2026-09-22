from sentence_transformers import SentenceTransformer
from db.qdrant import client, COLLECTION_NAME

MODEL = "nomic-ai/nomic-embed-text-v1.5"
model = SentenceTransformer(MODEL, trust_remote_code=True)

def retrieve(query:str, limit:int = 5):
    response= model.encode(
        model = MODEL,
        input=query
    )


    query_embedding = response["embeddings"][0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query = query_embedding,
        limit=limit,
    )


    return [
        point.payload
        for point in results.points
    ]

