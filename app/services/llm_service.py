from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
)

MODEL_NAME = "qwen_qwen3-0.6b"


def generate_answer(
    question: str,
    context: str,
) -> str:

    prompt = f"""
/no_think

You are answering a question from a document.

Use ONLY the information in the CONTEXT.

CONTEXT:
{context}

QUESTION:
{question}

INSTRUCTION:
Give the direct answer to the question.
Do not say you don't know if the answer is explicitly present in the context.
Do not add information that is not in the context.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
        max_tokens=100,
    )

    return response.choices[0].message.content.strip()