from llm.chat import llm


def verify_answer(
    question: str,
    answer: str,
    context: str
):

    prompt = f"""
You are a citation verification system for a RAG application.

Your task is to determine whether the answer is fully supported by the provided context.

Question:
{question}

Context:
{context}

Answer:
{answer}

Rules:
- Check only whether the answer is supported by the context.
- Do not use outside knowledge.
- If every factual claim in the answer is supported by the context, return exactly: SUPPORTED
- If any factual claim is unsupported, return exactly: UNSUPPORTED
- Do not provide explanations.
- Do not return anything except SUPPORTED or UNSUPPORTED.
"""

    response = llm.invoke(
        [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.content.strip().upper()

    return result == "SUPPORTED"