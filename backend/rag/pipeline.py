from retrieval.retriever import retriever
from llm.chat import chat
from rag.query_rewriter import rewrite_query
from rag.context_filter import filter_context
from rag.citation_verifier import verify_answer

def build_context(results):
    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['filename']}\n"
            f"{result['text']}"
        )

    return "\n\n".join(context_parts)


def rag_pipeline(question: str, history: str = ""):

    search_query = rewrite_query(
        question=question,
        history=history
    )

    results = retriever(
        search_query,
        limit=5
    )

    results = filter_context(
    results,
    threshold=0.0,
    max_chunks=3
)

    if not results:
        return {
            "answer": "I could not find relevant information in the provided documents.",
            "sources": []
        }

    context = build_context(results)

    answer = chat(
        question=question,
        context=context,
        history=history
    )

    supported = verify_answer(
        question=question,
        answer=answer,
        context=context
    )

    sources = []

    for result in results:
        sources.append(
    {
        "filename": result["filename"],
        "document_id": result["document_id"],
        "page": result["page"],
        "chunk_index": result["chunk_index"],
        "rerank_score": result.get("rerank_score")
    }
)

        return {
        "answer": answer,
        "sources": sources,
        "citation_verified": supported
    }