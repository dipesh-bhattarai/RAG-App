import logging
import time

from retrieval.retriever import retriever
from llm.chat import chat
from rag.query_rewriter import rewrite_query
from rag.context_filter import filter_context
from rag.citation_verifier import verify_answer


logger = logging.getLogger(__name__)


def build_context(results):
    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['filename']}\n"
            f"{result['text']}"
        )

    return "\n\n".join(context_parts)


def rag_pipeline(question: str, history: str = ""):

    total_start = time.perf_counter()

    logger.info(
        "RAG request started | question=%s",
        question
    )

    # Query rewriting
    start = time.perf_counter()

    search_query = rewrite_query(
        question=question,
        history=history
    )

    rewrite_time = time.perf_counter() - start

    logger.info(
        "Query rewriting completed | latency=%.2fs | query=%s",
        rewrite_time,
        search_query
    )

    # Retrieval
    start = time.perf_counter()

    results = retriever(
        search_query,
        limit=5
    )

    retrieval_time = time.perf_counter() - start

    logger.info(
        "Retrieval completed | latency=%.2fs | results=%d",
        retrieval_time,
        len(results)
    )

    # Context filtering
    results = filter_context(
        results,
        threshold=0.0,
        max_chunks=3
    )

    logger.info(
        "Context filtering completed | chunks=%d",
        len(results)
    )

    if not results:

        total_time = time.perf_counter() - total_start

        logger.warning(
            "No relevant context found | total_latency=%.2fs",
            total_time
        )

        return {
            "answer": "I could not find relevant information in the provided documents.",
            "sources": [],
            "citation_verified": False
        }

    context = build_context(results)

    # LLM generation
    start = time.perf_counter()

    answer = chat(
        question=question,
        context=context,
        history=history
    )

    llm_time = time.perf_counter() - start

    logger.info(
        "LLM generation completed | latency=%.2fs",
        llm_time
    )

    # Citation verification
    start = time.perf_counter()

    supported = verify_answer(
        question=question,
        answer=answer,
        context=context
    )

    verification_time = time.perf_counter() - start

    logger.info(
        "Citation verification completed | latency=%.2fs | verified=%s",
        verification_time,
        supported
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

    total_time = time.perf_counter() - total_start

    logger.info(
        "RAG request completed | total_latency=%.2fs | sources=%d",
        total_time,
        len(sources)
    )

    return {
        "answer": answer,
        "sources": sources,
        "citation_verified": supported
    }