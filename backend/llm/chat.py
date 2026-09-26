from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def chat(question: str, context: str, history: str = ""):

    prompt = f"""
You are a helpful and accurate RAG assistant.

Answer the user's question using ONLY the information provided in the context.

Rules:
- Do not use outside knowledge.
- Do not invent or assume information.
- If the answer cannot be found in the context, clearly say that the information is not available in the provided documents.
- Give a concise and direct answer.
- Use the conversation history only to understand references in the user's question.
- Do not treat conversation history as a source of factual information.

Context:
{context}

Conversation History:
{history}

Question:
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

    return response.content