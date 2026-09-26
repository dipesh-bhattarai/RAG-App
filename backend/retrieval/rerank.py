from sentence_transformers import CrossEncoder


MODEL = "BAAI/bge-reranker-v2-m3"

model = None


def get_reranker():
    global model

    if model is None:
        model = CrossEncoder(MODEL)

    return model


def rerank(question, chunks):
    if not chunks:
        return []

    model = get_reranker()

    pairs = [
        (question, chunk["text"])
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    ranked = []

    for chunk, score in zip(chunks, scores):
        ranked.append(
            {
                **chunk,
                "rerank_score": float(score)
            }
        )

    ranked.sort(
        key=lambda item: item["rerank_score"],
        reverse=True
    )

    return ranked