from retrieval.hybrid_search import hybrid_search


def retriever(query, limit=5):
    return hybrid_search(query, limit)
