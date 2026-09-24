from retrieval.keyword_search import keyword_search
from retrieval.rerank import rerank
from retrieval.vector_search import vector_search


def hybrid_search(question, limit=5):

    vector_results = vector_search(
        question,
        limit * 4
    )

    keyword_results = keyword_search(
        question,
        limit * 4
    )

    merged = {}

    # Add vector search results
    for chunk in vector_results:
        key = (
            chunk["document_id"],
            chunk["chunk_index"],
        )

        merged[key] = chunk

    # Add keyword search results
    for chunk in keyword_results:
        key = (
            chunk["document_id"],
            chunk["chunk_index"]
        )

        if key not in merged:
            merged[key] = chunk

    # Convert merged dictionary to list
    results = list(
        merged.values()
    )

    # Rerank merged results
    results = rerank(
        question,
        results
    )

    # Return the actual results
    return results