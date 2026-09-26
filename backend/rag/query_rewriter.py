from llm.chat import llm


def rewrite_query(question: str, history: str = ""):

    if not history.strip():
        return question

    prompt = f"""
Rewrite the user's latest question into a standalone search query.

Use the conversation history only to resolve references such as:
- he / she / they
- it / that / those
- this / these
- previous topics

Rules:
- Preserve the user's original intent.
- Do not answer the question.
- Do not add information that is not present in the question or history.
- If the question is already standalone, return it unchanged.
- Return ONLY the rewritten search query.
- Do not use quotation marks.
- Keep it concise.

Conversation History:
{history}

Latest User Question:
{question}
"""

    response = llm.invoke(
        [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content.strip()