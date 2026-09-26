def filter_context(
    results,
    threshold=0.0,
    max_chunks=3
):
    if not results:
        return []

    filtered = [
        result
        for result in results
        if result.get("rerank_score", 0) >= threshold
    ]

    return filtered[:max_chunks]