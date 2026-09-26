import os
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams
)
from uuid import uuid4

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if QDRANT_URL:
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )
else:
    client = QdrantClient(
        "localhost",
        port=6333
    )

COLLECTION_NAME = "documents"

def create_collection(vector_size: int):
    collections = client.get_collections().collections

    exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections
    )

    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

    # Create payload index for document filtering
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="document_id",
        field_schema="keyword"
    )


def store_embeddings(embeddings):

    batch_size = 10

    for start in range(0, len(embeddings), batch_size):

        batch = embeddings[start:start + batch_size]

        points = []

        for item in batch:

            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=item["embedding"],
                    payload={
                        "text": item["text"],
                        "filename": item["filename"],
                        "document_id": item["document_id"],
                        "page": item["page"],
                        "chunk_index": item["chunk_index"],
                    }
                )
            )

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

def list_document():
    documents = {}

    offset = None

    while True:
        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
            with_vectors=False,
            offset=offset
        )

        for point in points:
            payload = point.payload

            document_id = payload["document_id"]

            if document_id not in documents:
                documents[document_id] = {
                    "document_id": document_id,
                    "filename": payload["filename"],
                    "chunks": 0
                }

            documents[document_id]["chunks"] += 1

        if offset is None:
            break

    return list(documents.values())

def delete_document(document_id):
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key = "document_id",
                    match= MatchValue(
                        value=document_id
                    )
                )
            ]
        )
    )

def list_chunks():
    chunks = []

    offset = None

    while True:
        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
            with_vectors=False,
            offset=offset
        )

        for point in points:
            chunks.append(
    {
        "text": point.payload["text"],
        "filename": point.payload["filename"],
        "document_id": point.payload["document_id"],
        "page": point.payload["page"],
        "chunk_index": point.payload["chunk_index"],
    }
)

        if offset is None:
            break

    return chunks
    
        