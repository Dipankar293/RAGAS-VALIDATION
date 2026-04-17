# STEP 6: OpenAI Answer Generation

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(query, retrieved_chunks):
    """
    Generate grounded answer using OpenAI
    """

    # 🔹 Combine context
    context = "\n\n".join([chunk["content"] for chunk in retrieved_chunks])

    # 🔹 Strong prompt (VERY IMPORTANT)
    prompt = f"""
You are an expert assistant.

Answer the question ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-5",  # fast + cheap + good
        messages=[
            {"role": "system", "content": "You answer only from provided context."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

