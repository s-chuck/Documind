# # from openai import OpenAI


# # client = OpenAI(
# #     base_url="http://localhost:1234/v1",
# #     api_key="lm-studio",
# # )

# # MODEL_NAME = "qwen_qwen3-0.6b"


# # def generate_answer(
# #     question: str,
# #     context: str,
# # ) -> str:

# #     prompt = f"""
# # /no_think

# # You are answering a question from a document.

# # Use ONLY the information in the CONTEXT.

# # CONTEXT:
# # {context}

# # QUESTION:
# # {question}

# # INSTRUCTION:
# # Give the direct answer to the question.
# # Do not say you don't know if the answer is explicitly present in the context.
# # Do not add information that is not in the context.
# # """

# #     print("===== CONTEXT SENT TO LLM =====")
# #     print(context)
# #     print("===== END CONTEXT =====")
# #     response = client.chat.completions.create(
# #         model=MODEL_NAME,
# #         messages=[
# #             {
# #                 "role": "user",
# #                 "content": prompt,
# #             }
# #         ],
# #         temperature=0,
# #         max_tokens=300,
# #     )
# #     print("===== LLM RESPONSE =====")
# #     print(repr(response.choices[0].message.content))
# #     print("===== END RESPONSE =====")

# #     return response.choices[0].message.content.strip()

# from openai import OpenAI


# client = OpenAI(
#     base_url="http://localhost:1234/v1",
#     api_key="lm-studio",
# )

# MODEL_NAME = "qwen_qwen3-0.6b"


# def generate_answer(
#     question: str,
#     context: str,
# ) -> str:

#     prompt = f"""
# Answer the QUESTION using only the CONTEXT.

# Rules:
# - Answer exactly what the question asks.
# - Do not substitute a related number or fact.
# - Do not guess or infer missing information.
# - If the context does not establish the answer, say "The provided document does not specify this."
# - "Not mentioned" does not mean "No."
# - Preserve numbers and limits exactly.
# - Give only the final answer. Do not provide reasoning.

# CONTEXT:

# {context}

# QUESTION:

# {question}

# INSTRUCTION:

# Give the direct answer to the question.

# Do not say you don't know if the answer is explicitly present in the context.

# Do not add information that is not in the context.

# ANSWER:
# /no_think
# """

#     print("\n===== LLM DEBUG =====")
#     print("MODEL:", MODEL_NAME)
#     print("QUESTION:")
#     print(question)

#     print("\n===== CONTEXT SENT TO LLM =====")
#     print(context)
#     print("===== END CONTEXT =====")

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt,
#                 }
#             ],
#             temperature=0,
#             max_tokens=300,
#         )

#         choice = response.choices[0]

#         print("\n===== LLM RESPONSE DEBUG =====")

#         print("FINISH REASON:")
#         print(choice.finish_reason)

#         print("\nMESSAGE:")
#         print(choice.message)

#         print("\nCONTENT:")
#         print(repr(choice.message.content))

#         print("\nUSAGE:")
#         print(response.usage)

#         print("===== END LLM RESPONSE DEBUG =====\n")

#         content = choice.message.content

#         if content is None:
#             return ""

#         return content.strip()

#     except Exception as e:
#         print("\n===== LLM ERROR =====")
#         print(type(e).__name__)
#         print(str(e))
#         print("===== END LLM ERROR =====\n")

#         return ""



import os

from openai import OpenAI


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL_NAME = "cohere/north-mini-code:free"


def generate_answer(
    question: str,
    context: str,
) -> str:

    prompt = f"""
/no_think

Answer the QUESTION using only the CONTEXT.

Rules:

- Answer exactly what the question asks.
- Do not substitute a related number or fact.
- Do not guess or infer missing information.
- If the context does not establish the answer, say "The provided document does not specify this."
- "Not mentioned" does not mean "No."
- Preserve numbers and limits exactly.
- Give only the final answer. Do not provide reasoning.

CONTEXT:

{context}

QUESTION:

{question}

INSTRUCTION:

Give the direct answer to the question.

Do not say you don't know if the answer is explicitly present in the context.

Do not add information that is not in the context.

ANSWER:
"""

    print("\n===== LLM DEBUG =====")
    print("MODEL:", MODEL_NAME)
    print("QUESTION:")
    print(question)

    print("\n===== CONTEXT SENT TO LLM =====")
    print(context)
    print("===== END CONTEXT =====")

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
            max_tokens=600,
        )

        choice = response.choices[0]

        print("\n===== LLM RESPONSE DEBUG =====")

        print("FINISH REASON:")
        print(choice.finish_reason)

        print("\nMESSAGE:")
        print(choice.message)

        print("\nCONTENT:")
        print(repr(choice.message.content))

        print("\nUSAGE:")
        print(response.usage)

        print("===== END LLM RESPONSE DEBUG =====\n")

        content = choice.message.content

        if content is None:
            return ""

        return content.strip()

    except Exception as e:

        print("\n===== LLM ERROR =====")
        print(type(e).__name__)
        print(str(e))
        print("===== END LLM ERROR =====\n")

        return ""