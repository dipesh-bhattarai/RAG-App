from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

def chat(question: str, context:str, history:str):
    prompt = f"""
You are a helpful assistant.
Anawer only using the provided context.
Context:{context}
Question:{question}
History:{history}
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


